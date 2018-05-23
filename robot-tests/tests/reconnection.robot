*** Settings ***
Library       Collections
Resource      ../global_vars.robot

Library       libs.Cleaner    WITH NAME    Cleaner
Library       libs.ConnectivityChecker    WITH NAME     Checker
Library       libs.ControllerAdapter    ${CONTROLLER_ENDPOINT}    WITH NAME    Controller

Test Setup    Log To Console    Using Controller endpoint ${CONTROLLER_ENDPOINT}

Force Tags     reconnection_suite    sdn_workshop

*** Variables ***
${CONTROLLER_ENDPOINT}    ${CONTROLLER_IP}:${CONTROLLER_PORT}

*** Keywords ***
Perform Teardown
    [Arguments]    ${network_name}
    Controller.Clean Data
    Cleaner.Remove Network    ${network_name}


*** Test Cases ***
Create Remove logical port
    [Tags]    reconnection_1    time_consuming
    [Documentation]  Tests whether the same port can be added and removed more times than different ipam pools count
    ${network_a}    Set Variable    Network-A
    ${repeat_times}    Set Variable    33
    Controller.Create Network    ${network_a}    192.168.0.0/24
    Controller.Create Remove Repeat Logical Port    ${network_a}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}    ${repeat_times}
    Controller.Create Logical Port    ${network_a}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.10
    Run Keyword If    ${result} == ${False}    Fail

    Controller.Remove Logical Port    ${network_a}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.10
    Run Keyword If    ${result} == ${True}    Fail


    [Teardown]    Perform Teardown    ${network_a}

Recreate logical port
    [Tags]    reconnection_2
    [Documentation]  Tests if everything works after logical port was recreated
    ${network_a}    Set Variable    Network-A
    Controller.Create Network    ${network_a}    192.168.0.0/24
    Controller.Create Logical Port    ${network_a}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}
    Controller.Create Logical Port    ${network_a}    ${AGENT_OLA_ID}    ${AGENT_OLA_IP}

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.2
    Run Keyword If    ${result} == ${False}    Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.11
    Run Keyword If    ${result} == ${False}    Fail

    Controller.Remove Logical Port    ${network_a}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.2
    Run Keyword If    ${result} == ${True}    Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.11
    Run Keyword If    ${result} == ${True}    Fail

    Controller.Create Logical Port    ${network_a}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.18
    Run Keyword If    ${result} == ${False}    Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.11
    Run Keyword If    ${result} == ${False}    Fail


    [Teardown]    Perform Teardown    ${network_a}



















