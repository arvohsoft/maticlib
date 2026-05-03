import pytest
import logging
from maticlib.vectorstores.config import VectorIndexConfig, IndexingStrategy


def test_config_performance_profile_fast():
    config = VectorIndexConfig(performance_profile="fast")
    assert config.strategy == IndexingStrategy.HNSW
    assert config.hnsw_m == 8
    assert config.hnsw_ef_construction == 100


def test_config_performance_profile_balanced():
    config = VectorIndexConfig(performance_profile="balanced")
    assert config.strategy == IndexingStrategy.HNSW
    assert config.hnsw_m == 16
    assert config.hnsw_ef_construction == 200


def test_config_performance_profile_accurate():
    config = VectorIndexConfig(performance_profile="accurate")
    assert config.strategy == IndexingStrategy.FLAT


def test_config_default_is_balanced():
    config = VectorIndexConfig()
    assert config.strategy == IndexingStrategy.HNSW
    assert config.hnsw_m == 16


def test_config_strategy_overrides_profile(caplog):
    # If both are provided, strategy wins, and a warning is logged
    with caplog.at_level(logging.WARNING):
        config = VectorIndexConfig(
            performance_profile="fast", strategy=IndexingStrategy.IVF
        )

    assert config.strategy == IndexingStrategy.IVF
    assert "both strategy and performance_profile provided" in caplog.text


def test_config_custom_parameters():
    config = VectorIndexConfig(
        strategy=IndexingStrategy.HNSW, distance_metric="l2", collection_name="test_col"
    )
    assert config.strategy == IndexingStrategy.HNSW
    assert config.distance_metric == "l2"
    assert config.collection_name == "test_col"
