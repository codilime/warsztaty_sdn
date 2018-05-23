*** Settings ***
Library       Collections
Resource      ../global_vars.robot

Library       libs.Cleaner    WITH NAME    Cleaner
Library       libs.ConnectivityChecker    WITH NAME     Checker
Library       libs.ControllerAdapter    ${CONTROLLER_ENDPOINT}    WITH NAME    Controller

Test Setup    Log To Console    Using Controller endpoint ${CONTROLLER_ENDPOINT}

Force Tags     crud_suite    sdn_workshop

*** Variables ***
${CONTROLLER_ENDPOINT}    ${CONTROLLER_IP}:${CONTROLLER_PORT}

*** Keywords ***


*** Test Cases ***
Create Remove logical port
    [Tags]    multiple_networks_1
    [Documentation]  Tests create and remove logical port
    ${network_a}    Set Variable    Network-A
    Controller.Create Network    ${network_a}    192.168.0.0/24
    Controller.Create Logical Port    ${network_a}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}
    Controller.Create Logical Port    ${network_a}    ${AGENT_KASIA_ID}    ${AGENT_KASIA_IP}

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    127.0.0.1
    Run Keyword If    ${result} == ${False}   Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.2
    Run Keyword If    ${result} == ${False}    Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.11
    Run Keyword If    ${result} == ${False}    Fail

    Controller.Remove Logical Port    ${network_a}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.2
    Run Keyword If    ${result} == ${True}    Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.11
    Run Keyword If    ${result} == ${True}    Fail


    [Teardown]    Run Keywords    Controller.Clean Data
    ...           AND    Cleaner.Remove Network    ${network_a}


Remove in first add in second
    [Tags]    multiple_networks_2
    [Documentation]  Tests creating logical port in second network after removing in a first network
    ${network_a}    Set Variable    Network-A
    ${network_b}    Set Variable    Network-B

    Controller.Create Network    ${network_a}    192.168.0.0/24
    Controller.Create Logical Port    ${network_a}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}
    Controller.Create Logical Port    ${network_a}    ${AGENT_OLA_ID}    ${AGENT_OLA_IP}

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.2
    Run Keyword If    ${result} == ${False}    Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.11
    Run Keyword If    ${result} == ${False}    Fail

    Controller.Remove Logical Port    ${network_a}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}
    Controller.Create Network    ${network_b}    192.168.1.0/24
    Controller.Create Logical Port    ${network_b}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}
    Controller.Create Logical Port    ${network_b}    ${AGENT_OLA_ID}    ${AGENT_OLA_IP}

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.1.2
    Run Keyword If    ${result} == ${False}    Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.1.11
    Run Keyword If    ${result} == ${False}    Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.2
    Run Keyword If    ${result} == ${True}    Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.11
    Run Keyword If    ${result} == ${True}    Fail

    [Teardown]    Run Keywords    Controller.Clean Data
    ...           AND    Cleaner.Remove Network    ${network_a}
    ...           AND    Cleaner.Remove Network    ${network_b}

One cotainer two networks
    [Tags]    multiple_networks_3
    [Documentation]  Tests creating logical ports in two networks for the same container
    ${network_a}    Set Variable    Network-A
    ${network_b}    Set Variable    Network-B

    Controller.Create Network    ${network_a}    192.168.0.0/24
    Controller.Create Logical Port    ${network_a}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}
    Controller.Create Logical Port    ${network_a}    ${AGENT_OLA_ID}    ${AGENT_OLA_IP}

    Controller.Create Network    ${network_b}    192.168.1.0/24
    Controller.Create Logical Port    ${network_b}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}
    Controller.Create Logical Port    ${network_b}    ${AGENT_OLA_ID}    ${AGENT_OLA_IP}

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.2
    Run Keyword If    ${result} == ${False}    Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.11
    Run Keyword If    ${result} == ${False}    Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.1.2
    Run Keyword If    ${result} == ${False}    Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.1.11
    Run Keyword If    ${result} == ${False}    Fail



    ${result}    Checker.Ping    ${AGENT_OLA_IP}:${AGENT_OLA_PORT}    192.168.0.10
    Run Keyword If    ${result} == ${False}    Fail

    ${result}    Checker.Ping    ${AGENT_OLA_IP}:${AGENT_OLA_PORT}    192.168.0.3
    Run Keyword If    ${result} == ${False}    Fail

    ${result}    Checker.Ping    ${AGENT_OLA_IP}:${AGENT_OLA_PORT}    192.168.1.10
    Run Keyword If    ${result} == ${False}    Fail

    ${result}    Checker.Ping    ${AGENT_OLA_IP}:${AGENT_OLA_PORT}    192.168.1.3
    Run Keyword If    ${result} == ${False}    Fail


    [Teardown]    Run Keywords    Controller.Clean Data
    ...           AND    Cleaner.Remove Network    ${network_a}
    ...           AND    Cleaner.Remove Network    ${network_b}





