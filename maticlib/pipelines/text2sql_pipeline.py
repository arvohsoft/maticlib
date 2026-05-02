from typing import Optional, Tuple, List, Any
from maticlib.core.text2sql.loaders import BaseSchemaLoader
from maticlib.core.text2sql.executors import BaseExecutor
from maticlib.core.text2sql.guards import SQLInjectionGuard
from maticlib.prompts.registry import PromptRegistry
from maticlib.observability.trace import PipelineTrace, StepTrace
from maticlib.exceptions import SQLValidationError, SQLInjectionError
import time

class Text2SQLPipeline:
    """
    End-to-end Text2SQL pipeline.
    """
    def __init__(
        self,
        llm_client: Any,
        schema_loader: BaseSchemaLoader,
        executor: BaseExecutor,
        connection_string: str,
        dialect: str = "sqlite"
    ):
        self.llm_client = llm_client
        self.schema_loader = schema_loader
        self.executor = executor
        self.connection_string = connection_string
        self.dialect = dialect
        
        self.guard = SQLInjectionGuard(allowed_dialect=dialect)
        self.prompt_template = PromptRegistry.get("text2sql_generation")

    def execute(
        self, 
        question: str, 
        trace: Optional[PipelineTrace] = None
    ) -> Tuple[List[str], List[Tuple]]:
        """
        Translates a question to SQL, validates it, and executes it.
        Returns columns and rows.
        """
        # Step 1: Schema Loading
        schema_step = StepTrace(step_name="Schema_Load") if trace else None
        try:
            schema = self.schema_loader.load_schema(self.connection_string)
            schema_str = schema.to_prompt_string()
        finally:
            if trace and schema_step:
                schema_step.end_time = time.time()
                trace.add_step(schema_step)

        # Step 2: SQL Generation
        gen_step = StepTrace(step_name="SQL_Generation") if trace else None
        try:
            prompt = self.prompt_template.format(
                schema=schema_str,
                dialect=self.dialect,
                question=question
            )
            res = self.llm_client.complete(prompt)
            
            if hasattr(res, 'prompt_tokens') and trace and gen_step:
                gen_step.prompt_tokens = getattr(res, 'prompt_tokens', 0)
                gen_step.completion_tokens = getattr(res, 'completion_tokens', 0)
                gen_step.total_tokens = getattr(res, 'total_tokens', 0)
                
            raw_sql = self.llm_client.get_text_response(res)
            
            # Clean up markdown if LLM wrapped it
            raw_sql = raw_sql.strip("` \n")
            if raw_sql.startswith("sql"):
                raw_sql = raw_sql[3:].strip()
                
        finally:
            if trace and gen_step:
                gen_step.end_time = time.time()
                trace.add_step(gen_step)

        # Step 3: Validation and Execution
        exec_step = StepTrace(step_name="SQL_Execution") if trace else None
        try:
            safe_query = self.guard.validate_and_format(raw_sql)
            columns, rows = self.executor.execute(safe_query)
            return columns, rows
        except (SQLValidationError, SQLInjectionError) as e:
            if exec_step: exec_step.error = str(e)
            raise
        except Exception as e:
            if exec_step: exec_step.error = f"Execution failed: {e}"
            raise
        finally:
            if trace and exec_step:
                exec_step.end_time = time.time()
                trace.add_step(exec_step)
