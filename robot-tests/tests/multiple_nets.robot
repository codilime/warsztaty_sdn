*** Settings ***
Library       Collections
Resource      ../global_vars.robot

Library       libs.Cleaner    WITH NAME    Cleaner
Library       libs.ConnectivityChecker    WITH NAME     Checker
Library       libs.ControllerAdapter    ${CONTROLLER_ENDPOINT}    WITH NAME    Controller

Test Setup    Log To Console    Using Controller endpoint ${CONTROLLER_ENDPOINT}

Force Tags     basic_suite    sdn_workshop

*** Variables ***
${CONTROLLER_ENDPOINT}    ${CONTROLLER_IP}:${CONTROLLER_PORT}

*** Keywords ***
Perform Teardown One Network
    [Arguments]    ${network_name}
    Controller.Clean Data
    Cleaner.Remove Network    ${network_name}

Perform Teardown Two Networks
    [Arguments]    ${network_name_a}    ${network_name_b}
    Controller.Clean Data
    Cleaner.Remove Network    ${network_name_a}
    Cleaner.Remove Network    ${network_name_b}

*** Test Cases ***
Create Remove logical port
    [Tags]    multiple_networks_1
    [Documentation]  .....
    ${network_a}    Set Variable    Network-A
    Controller.Create Network    ${network_a}    192.168.0.0/24
    Controller.Create Logical Port    ${network_a}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    127.0.0.1
    Run Keyword If    ${result} == ${False}   Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.2
    Run Keyword If    ${result} == ${False}    Fail

    Controller.Remove Logical Port    ${network_a}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.2
    Run Keyword If    ${result} == ${True}    Fail


    [Teardown]    Perform Teardown One Network    ${network_a}


Remove in first add in second
    [Tags]    multiple_networks_2
    [Documentation]  .....
    ${network_a}    Set Variable    Network-A
    ${network_b}    Set Variable    Network-B

    Controller.Create Network    ${network_a}    192.168.0.0/24
    Controller.Create Logical Port    ${network_a}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.2
    Run Keyword If    ${result} == ${False}    Fail

    Controller.Remove Logical Port    ${network_a}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}
    Controller.Create Network    ${network_b}    192.168.1.0/24
    Controller.Create Logical Port    ${network_b}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    127.0.0.1
    Run Keyword If    ${result} == ${False}   Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.1.2
    Run Keyword If    ${result} == ${False}    Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.2
    Run Keyword If    ${result} == ${True}    Fail

    [Teardown]    Perform Teardown Two Networks    ${network_a}    ${network_b}

One cotainer two networks
    [Tags]    multiple_networks_3
    [Documentation]  .....
    ${network_a}    Set Variable    Network-A
    ${network_b}    Set Variable    Network-B

    Controller.Create Network    ${network_a}    192.168.0.0/24
    Controller.Create Logical Port    ${network_a}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}

    Controller.Create Network    ${network_b}    192.168.1.0/24
    Controller.Create Logical Port    ${network_b}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    127.0.0.1
    Run Keyword If    ${result} == ${False}   Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.2
    Run Keyword If    ${result} == ${False}    Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.1.2
    Run Keyword If    ${result} == ${False}    Fail


    [Teardown]    Perform Teardown Two Networks    ${network_a}    ${network_b}





