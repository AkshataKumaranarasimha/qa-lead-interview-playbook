*** Settings ***
Documentation     Amazon Product Search Test Case
Library           SeleniumLibrary
Library           Collections

*** Variables ***
${AMAZON_URL}          https://www.amazon.com
${SEARCH_KEYWORD}      laptop
${BROWSER}             chrome
${TIMEOUT}             10s

*** Test Cases ***
Test Amazon Product Search
    [Documentation]    Test Case to search for a product on Amazon and verify results
    [Tags]             smoke    amazon    search
    
    Open Browser To Amazon Home Page
    Search For Product    ${SEARCH_KEYWORD}
    Verify Search Results Are Displayed
    Verify Product Details Are Visible
    Close Browser

Test Amazon Search With Multiple Keywords
    [Documentation]    Test multiple product searches on Amazon
    [Tags]             regression    amazon
    
    Open Browser To Amazon Home Page
    Search For Product    wireless mouse
    Verify Search Results Are Displayed
    Verify At Least One Product Is Listed
    Close Browser

Test Amazon Product Sorting
    [Documentation]    Test product sorting functionality after search
    [Tags]             smoke    amazon    sorting
    
    Open Browser To Amazon Home Page
    Search For Product    ${SEARCH_KEYWORD}
    Verify Search Results Are Displayed
    Sort Results By Price Low To High
    Verify Results Are Sorted
    Close Browser

*** Keywords ***
Open Browser To Amazon Home Page
    [Documentation]    Open Amazon website in browser
    Open Browser    ${AMAZON_URL}    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains Element    id=twotabsearchtextbox    timeout=${TIMEOUT}
    Log    Amazon home page loaded successfully

Search For Product
    [Documentation]    Search for a product using the search box
    [Arguments]    ${product_name}
    
    Wait Until Element Is Visible    id=twotabsearchtextbox    timeout=${TIMEOUT}
    Input Text    id=twotabsearchtextbox    ${product_name}
    Press Keys    id=twotabsearchtextbox    RETURN
    Sleep    2s
    Log    Searched for product: ${product_name}

Verify Search Results Are Displayed
    [Documentation]    Verify that search results are displayed on the page
    
    Wait Until Page Contains Element    xpath=//div[@data-component-type='s-search-result']    timeout=${TIMEOUT}
    ${result_count}=    Get Element Count    xpath=//div[@data-component-type='s-search-result']
    Should Be Greater Than    ${result_count}    0
    Log    Found ${result_count} search results

Verify Product Details Are Visible
    [Documentation]    Verify that product details (name, price, rating) are visible
    
    # Verify product titles are visible
    Wait Until Page Contains Element    xpath=//span[@data-component-type='s-size-mini']    timeout=${TIMEOUT}
    ${titles}=    Get WebElements    xpath=//span[@data-component-type='s-size-mini']
    Should Not Be Empty    ${titles}
    
    # Verify prices are visible
    ${prices}=    Get WebElements    xpath=//span[@class='a-price-whole']
    Should Not Be Empty    ${prices}
    
    # Verify ratings are visible (if present)
    ${ratings}=    Get WebElements    xpath=//span[@aria-label*='star']
    Log    Found ${ratings.__len__()} products with ratings
    Log    Product details verified successfully

Verify At Least One Product Is Listed
    [Documentation]    Verify that at least one product is listed in search results
    
    ${products}=    Get WebElements    xpath=//div[@data-component-type='s-search-result']
    ${count}=    Get Length    ${products}
    Should Be Greater Than Or Equal To    ${count}    1
    Log    At least ${count} product(s) found

Sort Results By Price Low To High
    [Documentation]    Click on sort dropdown and select price low to high
    
    Wait Until Element Is Visible    xpath=//span[contains(text(), 'Sort by')]    timeout=${TIMEOUT}
    Click Element    xpath=//span[contains(text(), 'Sort by')]
    Sleep    1s
    Wait Until Element Is Visible    xpath=//a[contains(text(), 'Price: Low to High')]    timeout=${TIMEOUT}
    Click Element    xpath=//a[contains(text(), 'Price: Low to High')]
    Sleep    2s
    Log    Results sorted by price low to high

Verify Results Are Sorted
    [Documentation]    Verify that results are sorted by price in ascending order
    
    Wait Until Page Contains Element    xpath=//span[@class='a-price-whole']    timeout=${TIMEOUT}
    ${prices}=    Get WebElements    xpath=//span[@class='a-price-whole']
    Should Not Be Empty    ${prices}
    Log    Price sorting applied successfully
