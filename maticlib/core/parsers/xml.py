import re
import xml.etree.ElementTree as ET
from typing import Any, Dict
from maticlib.core.parsers.base import BaseResponseParser

class XMLResponseParser(BaseResponseParser[Dict[str, Any]]):
    """
    Parses LLM output into a dictionary using XML tags as structure.
    """
    
    def parse(self, text: str) -> Dict[str, Any]:
        """
        Extracts XML blocks and converts them into a flat dictionary.
        """
        # 1. Look for XML blocks in markdown or the whole text
        xml_match = re.search(r"```(?:xml)?\s*(<.*?>)\s*```", text, re.DOTALL | re.IGNORECASE)
        if xml_match:
            content = xml_match.group(1)
        else:
            # Try to find the first tag to the last tag
            content_match = re.search(r"(<.*?>.*</.*?>)", text, re.DOTALL)
            if not content_match:
                raise ValueError(f"Could not find any XML tags in response: {text}")
            content = content_match.group(1)
            
        try:
            # Wrap in a root tag to ensure valid XML for parsing
            wrapped_content = f"<root>{content}</root>"
            root = ET.fromstring(wrapped_content)
            
            # If the provided XML already had a single root tag (e.g. <user>...), 
            # and that tag has children, we want the children of THAT tag.
            if len(root) == 1 and list(root[0]):
                target = root[0]
            else:
                target = root
                
            return {child.tag: child.text for child in target}
        except ET.ParseError as e:
            raise ValueError(f"Could not parse response as XML: {e}\nContent: {content}")

    def get_structure_instructions(self) -> str:
        """
        Instructions for XML output.
        """
        return (
            "The output should be formatted as XML. "
            "Use clear tags for each data field. "
            "Respond strictly with the XML and no other text."
        )
