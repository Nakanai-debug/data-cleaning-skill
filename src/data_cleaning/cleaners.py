from __future__ import annotations
import re
from typing import Any, Iterable, Mapping
import pandas as pd


def standardize_name(name: str) -> str:
    value = re.sub(r"[^0-9a-zA-Z]+", "_", str(name).strip().lower())
    return re.sub(r"_+", "_", value).strip("_")


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result.columns = [standardize_name(c) for c in result.columns]
    return result


def clean_missing(df: pd.DataFrame, cfg: Mapping[str, Any]) -> pd.DataFrame:
    result = df.copy()
    strategy = cfg.get("strategy", "median")
    threshold = cfg.get("drop_threshold")
    if threshold is not None:
        result = result.loc[:, result.isna().mean() < float(threshold)]
    if strategy == "drop":
        return result.dropna()
    for column in result.columns:
        if not result[column].isna().any():
            continue
        if strategy == "constant":
            value = cfg.get("constant", "Unknown")
        elif pd.api.types.is_numeric_dtype(result[column]):
            value = result[column].mean() if strategy == "mean" else result[column].median()
        else:
            mode = result[column].mode(dropna=True)
            value = mode.iloc[0] if not mode.empty else cfg.get("constant", "Unknown")
        result[column] = result[column].fillna(value)
    return result


def clean_formats(df: pd.DataFrame, cfg: Mapping[str, Any]) -> pd.DataFrame:
    result = df.copy()
    date_cfg = cfg.get("dates", {})
    for column in date_cfg.get("columns", []):
        if column in result:
            result[column] = pd.to_datetime(result[column], errors="coerce", dayfirst=date_cfg.get("dayfirst", False))
    for column in cfg.get("numeric", {}).get("columns", []):
        if column in result:
            result[column] = pd.to_numeric(result[column], errors="coerce")
    text_cfg = cfg.get("text", {})
    for column in text_cfg.get("columns", []):
        if column in result:
            values = result[column].astype("string")
            if text_cfg.get("strip", True):
                values = values.str.strip()
            if text_cfg.get("lowercase", False):
                values = values.str.lower()
            result[column] = values
    return result


def clean_duplicates(df: pd.DataFrame, cfg: Mapping[str, Any]) -> pd.DataFrame:
    if not cfg.get("enabled", True):
        return df.copy()
    return df.drop_duplicates(subset=cfg.get("subset") or None, keep="first").reset_index(drop=True)


def correct_typos(df: pd.DataFrame, typo_map: Mapping[str, Any]) -> pd.DataFrame:
    result = df.copy()
    for column, replacements in typo_map.items():
        if column in result and isinstance(replacements, Mapping):
            result[column] = result[column].replace(dict(replacements))
    return result


def handle_outliers(df: pd.DataFrame, cfg: Mapping[str, Any]) -> pd.DataFrame:
    result = df.copy()
    if not cfg.get("enabled", False):
        return result
    columns: Iterable[str] = cfg.get("columns") or result.select_dtypes(include="number").columns
    for column in columns:
        if column not in result or not pd.api.types.is_numeric_dtype(result[column]):
            continue
        q1, q3 = result[column].quantile([0.25, 0.75])
        iqr = q3 - q1
        low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        if cfg.get("action", "clip") == "drop":
            result = result[result[column].between(low, high) | result[column].isna()]
        else:
            result[column] = result[column].clip(lower=low, upper=high)
    return result.reset_index(drop=True)
