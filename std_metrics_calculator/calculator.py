import asyncio
import json
from typing import Any

from core.metrics_calculator import (
    MetricsCalculator,
    MetricsCalculatorConfigShape,
    TreeMetrics,
)
from pydantic import ValidationError
from pydantic.alias_generators import to_snake


class StdMetricsCalculatorConfigShape(MetricsCalculatorConfigShape):
    cmd: str
    preprocess_keys: bool = False


def dict_to_snake_keys[T: dict[str, Any]](data: T) -> T:
    if type(data) is list:
        return [dict_to_snake_keys(el) for el in data]

    if type(data) is not dict:
        return data

    return {to_snake(k): dict_to_snake_keys(v) for k, v in data.items()}


class StdMetricsCalculator(
    MetricsCalculator[StdMetricsCalculatorConfigShape],
    config_shape=StdMetricsCalculatorConfigShape,
):
    async def calculate(self) -> TreeMetrics:
        proc = await asyncio.create_subprocess_shell(
            self.config.cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await proc.communicate(self.tree_data.model_dump_json().encode())

        if stderr:
            raise Exception(f'Error invoking std plugin: {stderr}')

        try:
            tree_metrics_dict = json.loads(stdout.decode())
            if self.config.preprocess_keys:
                tree_metrics_dict = dict_to_snake_keys(tree_metrics_dict)

            result = TreeMetrics.model_validate(tree_metrics_dict)
        except ValidationError as e:
            raise Exception('Plugin returned data in incompatible format:\n' + str(e))

        return result
