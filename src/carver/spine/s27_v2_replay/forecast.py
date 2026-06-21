from __future__ import annotations

from dataclasses import dataclass
from math import isclose

from ..m0 import CarverBlocked
from .identity import ReplayIdentity
from .validation import require_finite_number, require_hash, require_integer, require_positive_number, require_text


def _nonzero_sign(name: str, value: float) -> str:
    require_finite_number(name, value)
    if isclose(value, 0.0, rel_tol=0.0, abs_tol=1e-12):
        raise CarverBlocked(f"{name} must be nonzero until a zero-policy is source-locked")
    return "POSITIVE" if value > 0 else "NEGATIVE"


def _clamp_forecast(value: float) -> float:
    if value > 20.0:
        return 20.0
    if value < -20.0:
        return -20.0
    return value


def _is_zero(value: float) -> bool:
    return isclose(value, 0.0, rel_tol=0.0, abs_tol=1e-12)


@dataclass(frozen=True)
class ForecastReplayLedgerRow:
    identity: ReplayIdentity
    source_input_hash: str
    daily_runtime_hash: str
    ewma5_equilibrium_value: float
    ewma5_equilibrium_hash: str
    raw_mean_reversion_forecast_value: float
    raw_mean_reversion_forecast_hash: str
    sigma_bridge_price_value: float
    sigma_bridge_price_hash: str
    annual_percentage_sigma_value: float
    annual_percentage_sigma_hash: str
    sigma_price_value: float
    sigma_price_hash: str
    risk_adjusted_forecast_before_veto_value: float
    risk_adjusted_forecast_before_veto_hash: str
    ewmac16_64_trend_value: float
    ewmac16_64_trend_sign: str
    ewmac16_64_trend_hash: str
    trend_veto_decision: str
    trend_veto_decision_hash: str
    risk_adjusted_forecast_after_veto_value: float
    risk_adjusted_forecast_after_veto_hash: str
    relative_volatility_v_value: float
    relative_volatility_v_hash: str
    quantile_q_value: float
    quantile_q_hash: str
    raw_volatility_multiplier_value: float
    raw_volatility_multiplier_hash: str
    ewma10_multiplier_m_value: float
    ewma10_multiplier_m_hash: str
    risk_adjusted_after_veto_times_m_before_scalar_value: float
    risk_adjusted_after_veto_times_m_before_scalar_hash: str
    scalar_label: str
    scalar_value: float
    scalar_value_hash: str
    capped_forecast_value: float
    capped_forecast_hash: str
    desired_unrounded_position_value: float
    desired_unrounded_position_hash: str
    desired_rounded_position: int
    forecast_hash: str

    def validate(self) -> None:
        self.identity.validate()
        require_hash("S27 v2 forecast source input hash", self.source_input_hash)
        require_hash("S27 v2 forecast daily runtime hash", self.daily_runtime_hash)
        require_finite_number("S27 v2 EWMA5 equilibrium value", self.ewma5_equilibrium_value)
        require_hash("S27 v2 EWMA5 equilibrium hash", self.ewma5_equilibrium_hash)
        require_finite_number("S27 v2 raw mean-reversion forecast value", self.raw_mean_reversion_forecast_value)
        require_hash("S27 v2 raw mean-reversion forecast hash", self.raw_mean_reversion_forecast_hash)
        require_positive_number("S27 v2 sigma bridge price value", self.sigma_bridge_price_value)
        require_hash("S27 v2 sigma bridge price hash", self.sigma_bridge_price_hash)
        require_positive_number("S27 v2 annual percentage sigma value", self.annual_percentage_sigma_value)
        require_hash("S27 v2 annual percentage sigma hash", self.annual_percentage_sigma_hash)
        require_positive_number("S27 v2 sigma price value", self.sigma_price_value)
        require_hash("S27 v2 sigma price hash", self.sigma_price_hash)
        require_finite_number(
            "S27 v2 risk-adjusted forecast before veto value",
            self.risk_adjusted_forecast_before_veto_value,
        )
        require_hash(
            "S27 v2 risk-adjusted forecast before veto hash",
            self.risk_adjusted_forecast_before_veto_hash,
        )
        trend_value_sign = _nonzero_sign("S27 v2 EWMAC16/64 trend value", self.ewmac16_64_trend_value)
        require_text("S27 v2 EWMAC16/64 trend sign", self.ewmac16_64_trend_sign)
        if self.ewmac16_64_trend_sign not in ("POSITIVE", "NEGATIVE"):
            raise CarverBlocked("S27 v2 EWMAC16/64 trend sign must be POSITIVE or NEGATIVE")
        if self.ewmac16_64_trend_sign != trend_value_sign:
            raise CarverBlocked("S27 v2 EWMAC16/64 trend sign must match trend value")
        require_hash("S27 v2 EWMAC16/64 trend hash", self.ewmac16_64_trend_hash)
        require_text("S27 v2 trend veto decision", self.trend_veto_decision)
        if self.trend_veto_decision not in (
            "PERMIT_MEAN_REVERSION",
            "ZERO_FORECAST_BY_TREND_VETO",
            "FLAT_AT_EQUILIBRIUM",
        ):
            raise CarverBlocked("S27 v2 trend veto decision is unresolved")
        require_hash("S27 v2 trend veto decision hash", self.trend_veto_decision_hash)
        require_finite_number(
            "S27 v2 risk-adjusted forecast after veto value",
            self.risk_adjusted_forecast_after_veto_value,
        )
        require_hash(
            "S27 v2 risk-adjusted forecast after veto hash",
            self.risk_adjusted_forecast_after_veto_hash,
        )
        before_veto_is_zero = _is_zero(self.risk_adjusted_forecast_before_veto_value)
        if before_veto_is_zero:
            if self.trend_veto_decision != "FLAT_AT_EQUILIBRIUM":
                raise CarverBlocked("S27 v2 zero mean-reversion forecast must be source-labeled flat at equilibrium")
            if not _is_zero(self.risk_adjusted_forecast_after_veto_value):
                raise CarverBlocked("S27 v2 flat-at-equilibrium forecast after veto must be zero")
        else:
            before_veto_sign = _nonzero_sign(
                "S27 v2 risk-adjusted forecast before veto value",
                self.risk_adjusted_forecast_before_veto_value,
            )
            if before_veto_sign == self.ewmac16_64_trend_sign:
                if self.trend_veto_decision != "PERMIT_MEAN_REVERSION":
                    raise CarverBlocked("S27 v2 agreeing trend and mean-reversion signs must permit mean reversion")
                if not isclose(
                    self.risk_adjusted_forecast_after_veto_value,
                    self.risk_adjusted_forecast_before_veto_value,
                    rel_tol=0.0,
                    abs_tol=1e-12,
                ):
                    raise CarverBlocked("S27 v2 permitted trend veto must preserve pre-veto forecast")
            else:
                if self.trend_veto_decision != "ZERO_FORECAST_BY_TREND_VETO":
                    raise CarverBlocked("S27 v2 opposing trend and mean-reversion signs must zero forecast")
                if not _is_zero(self.risk_adjusted_forecast_after_veto_value):
                    raise CarverBlocked("S27 v2 trend-vetoed forecast must be zero")
        require_positive_number("S27 v2 relative volatility V value", self.relative_volatility_v_value)
        require_hash("S27 v2 relative volatility V hash", self.relative_volatility_v_hash)
        require_finite_number("S27 v2 quantile Q value", self.quantile_q_value)
        if self.quantile_q_value < 0 or self.quantile_q_value > 1:
            raise CarverBlocked("S27 v2 quantile Q value must be in [0, 1]")
        require_hash("S27 v2 quantile Q hash", self.quantile_q_hash)
        require_positive_number("S27 v2 raw volatility multiplier value", self.raw_volatility_multiplier_value)
        expected_raw_multiplier = 2.0 - (1.5 * self.quantile_q_value)
        if not isclose(self.raw_volatility_multiplier_value, expected_raw_multiplier, rel_tol=0.0, abs_tol=1e-12):
            raise CarverBlocked("S27 v2 raw volatility multiplier must equal 2 - 1.5 * Q")
        require_hash("S27 v2 raw volatility multiplier hash", self.raw_volatility_multiplier_hash)
        require_positive_number("S27 v2 EWMA10 multiplier M value", self.ewma10_multiplier_m_value)
        require_hash("S27 v2 EWMA10 multiplier M hash", self.ewma10_multiplier_m_hash)
        require_finite_number(
            "S27 v2 post-veto times M before scalar value",
            self.risk_adjusted_after_veto_times_m_before_scalar_value,
        )
        expected_post_veto_times_m = self.risk_adjusted_forecast_after_veto_value * self.ewma10_multiplier_m_value
        if not isclose(
            self.risk_adjusted_after_veto_times_m_before_scalar_value,
            expected_post_veto_times_m,
            rel_tol=0.0,
            abs_tol=1e-12,
        ):
            raise CarverBlocked("S27 v2 post-veto times M must equal post-veto forecast times EWMA10 multiplier M")
        require_hash(
            "S27 v2 post-veto times M before scalar hash",
            self.risk_adjusted_after_veto_times_m_before_scalar_hash,
        )
        require_text("S27 v2 scalar label", self.scalar_label)
        if self.scalar_label != "BOOK_APPROXIMATE_SCALAR_IMPLEMENTATION_FROZEN_AT_20_0":
            raise CarverBlocked("S27 v2 scalar label must preserve book-approximate implementation freeze")
        require_finite_number("S27 v2 scalar value", self.scalar_value)
        if self.scalar_value != 20.0:
            raise CarverBlocked("S27 v2 scalar value must be 20.0")
        require_hash("S27 v2 scalar value hash", self.scalar_value_hash)
        require_finite_number("S27 v2 capped forecast value", self.capped_forecast_value)
        if self.capped_forecast_value < -20 or self.capped_forecast_value > 20:
            raise CarverBlocked("S27 v2 capped forecast value must be in [-20, 20]")
        expected_capped_forecast = _clamp_forecast(
            self.risk_adjusted_after_veto_times_m_before_scalar_value * self.scalar_value
        )
        if not isclose(self.capped_forecast_value, expected_capped_forecast, rel_tol=0.0, abs_tol=1e-12):
            raise CarverBlocked("S27 v2 capped forecast must equal clamped post-veto times M times scalar")
        require_hash("S27 v2 capped forecast hash", self.capped_forecast_hash)
        require_finite_number("S27 v2 desired unrounded position value", self.desired_unrounded_position_value)
        if before_veto_is_zero:
            if not _is_zero(self.risk_adjusted_after_veto_times_m_before_scalar_value):
                raise CarverBlocked("S27 v2 flat-at-equilibrium post-veto times M must be zero")
            if not _is_zero(self.capped_forecast_value):
                raise CarverBlocked("S27 v2 flat-at-equilibrium capped forecast must be zero")
            if not _is_zero(self.desired_unrounded_position_value):
                raise CarverBlocked("S27 v2 flat-at-equilibrium desired unrounded position must be zero")
        require_hash("S27 v2 desired unrounded position hash", self.desired_unrounded_position_hash)
        require_integer("S27 v2 desired rounded position", self.desired_rounded_position)
        if before_veto_is_zero and self.desired_rounded_position != 0:
            raise CarverBlocked("S27 v2 flat-at-equilibrium desired rounded position must be zero")
        require_hash("S27 v2 forecast hash", self.forecast_hash)
