#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-


#<<<ilo_api_bios:sep(124)>>>
#Boot Mode|Uefi
#SR-IOV|Disabled
#Sub-Numa Clustering|Disabled

from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
)

from .agent_based_api.v1 import (
    register,
    Result,
    State,
    Service,
    Metric,
)

from .utils.hp_ilo import parse_hp_ilo

register.agent_section(
    name="ilo_api_bios",
    parse_function=parse_hp_ilo,
)


def discovery_ilo_api_bios(section) -> DiscoveryResult:
    for element in section:
        yield Service(item=element)


def check_ilo_api_bios(item: str, section) -> CheckResult:
    data = section.get(item)
    if data:
        setting, value = data
        state = State(0)
        match setting:
            case "Boot Mode":
                if value != "Uefi":
                    state = State(1)
            case "SR-IOV":
                if value != "Disabled":
                    state = State(1)
            case "Sub-Numa":
                if value != "Disabled":
                    state = State(1)
        yield Result(
            state=state,
            summary=f"{setting}: {value}"
        )


register.check_plugin(
    name="ilo_api_bios",
    service_name="BIOS %s",
    sections=["ilo_api_bios"],
    discovery_function=discovery_ilo_api_bios,
    check_function=check_ilo_api_bios,
)

