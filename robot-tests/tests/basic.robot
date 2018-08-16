*** Settings ***
Library       Collections
Resource      ../global_vars.robot

Library       libs.Cleaner    WITH NAME    Cleaner
Library       libs.ConnectivityChecker    WITH NAME     Checker
Library       libs.ControllerClient    ${CONTROLLER_ENDPOINT}    WITH NAME    Controller
Library       libs.DockerClient    WITH NAME    Docker

Test Setup    Log To Console    Using Controller endpoint ${CONTROLLER_ENDPOINT}

Force Tags     basic_suite    sdn_workshop

*** Variables ***
${CONTROLLER_ENDPOINT}    ${CONTROLLER_IP}:${CONTROLLER_PORT}

*** Keywords ***
Perform Teardown
    [Arguments]    ${network_name}
    Controller.Clean Data
    Cleaner.Remove Network    ${network_name}

*** Test Cases ***
Simplest VPN
    [Tags]   simple_vpn_1
    [Documentation]  Tests simple vpn 1-network-1-lp
    ${mynetwork}    Set Variable    Network-111
    ${myagent}    Set Variable    Ala-1

    Controller.Create Agent    ${myagent}
    Controller.Create Network    ${mynetwork}    192.168.0.0/24
    Controller.Create Logical Port    ${mynetwork}    ${myagent}
    ${myagent-ip}    Docker.Get Container Ip    ${myagent}

    # Sanity check
    ${result}    Checker.Ping    ${myagent-ip}:8090    127.0.0.1
    Run Keyword If    ${result} == ${False}   Fail

    ${result}    Checker.Ping    ${myagent-ip}:8090    192.168.0.2
    Run Keyword If    ${result} == ${False}    Fail

    [Teardown]    Perform Teardown    ${mynetwork}



Basic VPN
    [Tags]   simple_vpn_2
    [Documentation]  Tests simple vpn 1-network-2-lp

    ${mynetwork}    Set Variable    Network-111

    ${myagent-1}    Set Variable    Ala-1
    Controller.Create Agent    ${myagent-1}
    ${myagent-1-ip}    Docker.Get Container Ip    ${myagent-1}

    ${myagent-2}    Set Variable    Ola-1
    Controller.Create Agent    ${myagent-2}
    ${myagent-2-ip}    Docker.Get Container Ip    ${myagent-2}

    Controller.Create Network    ${mynetwork}    192.168.0.0/24
    Controller.Create Logical Port    ${mynetwork}    ${myagent-1}
    Controller.Create Logical Port    ${mynetwork}    ${myagent-2}

    ${result}    Checker.Ping    ${myagent-1-ip}:8090    192.168.0.2
    Run Keyword If    ${result} == ${False}    Fail

    ${result}    Checker.Ping    ${myagent-2-ip}:8090    192.168.0.11
    Run Keyword If    ${result} == ${False}    Fail

    [Teardown]    Perform Teardown    ${mynetwork}
