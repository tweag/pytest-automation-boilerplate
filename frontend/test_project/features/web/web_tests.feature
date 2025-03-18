@nondestructive @web_tests
Feature:  OrangeHRM Login and Modus QA blog

  @hrm_login @hrm_logout @automated @firefox @healthcheck
  Scenario: Login into OrangeHRM system and logout
    Given I set web base url '{%BASE_URL%}'
    And Browser is maximized
    And The title is 'OrangeHRM'
    When The element 'OrangeHRM > username' is displayed
    And I set text '{%HRM_USER_NAME%}' to field 'OrangeHRM > username'
    And I set text '{%HRM_PASSWORD%}' to field 'OrangeHRM > password'
    And I click on element 'OrangeHRM > login_button'
    Then The title is 'OrangeHRM'
    And The page url contains 'dashboard'
    When The element 'OrangeHRM > dashboard' is displayed
    And I click on element 'OrangeHRM > profile_menu'
    And I click item 'Logout' for element 'OrangeHRM > logout_button'
    Then The element 'OrangeHRM > username' is displayed

  @hrm_add_user @automated @firefox @smoke
  Scenario: Login and add admin user in OrangeHRM system
    Given I set web base url '{%BASE_URL%}'
    And Browser is maximized
    And The title is 'OrangeHRM'
    When The element 'OrangeHRM > username' is displayed
    And I set text '{%HRM_USER_NAME%}' to field 'OrangeHRM > username'
    And I set text '{%HRM_PASSWORD%}' to field 'OrangeHRM > password'
    And I click on element 'OrangeHRM > login_button'
    Then The title is 'OrangeHRM'
    And The page url contains 'dashboard'
    When The element 'OrangeHRM > dashboard' is displayed
    And I get text from element 'OrangeHRM > dashboard' and save as environment variable 'TEST_ONE'
    And I click item 'Admin' for element 'OrangeHRM > left_menu'
    When The element 'OrangeHRM > User > add_button' is displayed
    Then With soft assertion 'true' The page url contains '/admin/viewSystemUsers'
    When I click on button 'OrangeHRM > User > add_button'
    And I click item 'User Role' for element 'OrangeHRM > User > click_field'
    And I click item 'ESS' for element 'OrangeHRM > User > search_value'
    And I set value 'a' for item 'Employee Name' on element 'OrangeHRM > User > Input_field'
    And I pause for '3' s
    When I hover over 'OrangeHRM > User > select_value_2' and click element 'OrangeHRM > User > select_value_2'
    And I click item 'Status' for element 'OrangeHRM > User > click_field'
    And I click item 'Enabled' for element 'OrangeHRM > User > search_value'
    And I set value 'Tauqir_Sarwar' for item 'Username' on element 'OrangeHRM > User > Input_field'
    And I set value 'Test_123456' for item 'Password' on element 'OrangeHRM > User > Input_field'
    And I set value 'Test_123456' for item 'Confirm Password' on element 'OrangeHRM > User > Input_field'
    When The element 'OrangeHRM > User > save_button' is displayed
    When I click on button 'OrangeHRM > User > save_button'
    # flakiness in the application, success message is not displayed sometimes
#    When The element 'OrangeHRM > User > success_message' is displayed
    When The element 'OrangeHRM > User > add_button' is displayed
    And I set value 'Tauqir_Sarwar' for item 'Username' on element 'OrangeHRM > User > search_field'
    When I click on button 'OrangeHRM > User > search_button'
    Then I expect 'OrangeHRM > User > search_result' elements are present with innertext:
      | Tauqir_Sarwar |
      | ESS           |
    When I click on button 'OrangeHRM > User > delete_button'
    And I click on button 'OrangeHRM > User > delete_confirm'
    Then The element 'OrangeHRM > User > success_message' is displayed

  @blog_search @automated @firefox @sanity
  Scenario: Check QA modus blog Search
    Given I set web base url 'https://moduscreate.com'
    And The browser resolution is '1024' per '768'
    And The title is 'Modus Create | Digital Product Engineering Partner'
    When The element 'Modus_Site > main_heading' is displayed
    And I click item 'BLOG' for element 'Modus_Site > header_link'
    And The title is 'Blog | Digital Transformation Insights - Modus Create'
    When The element 'Modus_Site > dropdown' is displayed
#   Dropdown has some specific values now so can't select
#   And I select the option 'quality-assurance' by value for element 'Modus_Site > dropdown'
    And I pause for '5' s
    And I set text 'How to Avoid Flaky' to field 'Modus_Site > search_bar'
    When I click on button 'Modus_Site > search_icon'
    And The element 'Modus_Site > search_result' is displayed
    When I click on element 'Modus_Site > search_result'
    And The title is 'How to Avoid Flaky Tests? - Modus Create'
    And I scroll to element 'Modus_Site > blog_heading_1'
    And I scroll to element 'Modus_Site > blog_heading_2'
    And I scroll to element 'Modus_Site > blog_heading_1'
#    And The element 'Modus_Site > sub_popup_close' is displayed


  @sd_login @sd_login_error @sd_checkout @automated @firefox @sanity
  Scenario: Login into saucedemo site with valid credentials
    Given I set web base url 'https://www.saucedemo.com'
    And Browser is maximized
    And The title is 'Swag Labs'
    When The element 'SourceDemo_Site > username' is displayed
    And I set text 'invalid_user' to field 'SourceDemo_Site > username'
    And I set text 'invalid_pass' to field 'SourceDemo_Site > password'
    And I click on element 'SourceDemo_Site > login_button'
    When The element 'SourceDemo_Site > login_error_message' is displayed
    And I click on button 'SourceDemo_Site > login_error_message'
    And I clear text from field 'SourceDemo_Site > username'
    And I set text 'standard_user' to field 'SourceDemo_Site > username'
    And I clear text from field 'SourceDemo_Site > password'
    And I set text 'secret_sauce' to field 'SourceDemo_Site > password'
    And I click on element 'SourceDemo_Site > login_button'
    Then I expect that the title contains 'Swag'
    When The element 'SourceDemo_Site > menu_button' is displayed
    And I click item 'labs-backpack' for element 'SourceDemo_Site > add_product'
    And I click item 'labs-bike-light' for element 'SourceDemo_Site > add_product'
    And I click item 'labs-bike-light' for element 'SourceDemo_Site > remove_product'
    When The element 'SourceDemo_Site > cart_icon' text is '1'
    And I click on element 'SourceDemo_Site > cart_icon'
    When The element 'SourceDemo_Site > Checkout_page > checkout' is displayed
    And I click on element 'SourceDemo_Site > Checkout_page > checkout'
    When The element 'SourceDemo_Site > Checkout_page > first_name' is displayed
    And I set text 'Tauqir' to field 'SourceDemo_Site > Checkout_page > first_name'
    And I set text 'Sarwar' to field 'SourceDemo_Site > Checkout_page > last_name'
    And I set text '54810' to field 'SourceDemo_Site > Checkout_page > postal_code'
    And I click on button 'SourceDemo_Site > Checkout_page > continue'
    Then I expect that item 'Total: $32.39' for element 'SourceDemo_Site > Checkout_page > total_amount' is displayed
    When I click on button 'SourceDemo_Site > Checkout_page > finish'
    And The element 'SourceDemo_Site > Checkout_page > thank_you_message' is displayed


  @sd_failure_message @automated @firefox @regression
  Scenario: Try to login into saucedemo site with in-valid credentials
    Given I set web base url 'https://www.saucedemo.com'
    And Browser is maximized
    And The title is 'Swag Labs'
    When The element 'SourceDemo_Site > username' is displayed
    And I set text 'standard_user1' to field 'SourceDemo_Site > username'
    And I set text 'secret_sauce1' to field 'SourceDemo_Site > password'
    And I click on element 'SourceDemo_Site > login_button'
    Then The element 'SourceDemo_Site > login_error_message' is displayed

  @job_search @automated @healthcheck
  Scenario: Check QA modus job Search
    Given I set web base url 'https://moduscreate.com'
    And Browser is maximized
    And The title is 'Modus Create | Digital Product Engineering Partner'
    When The element 'Modus_Site > main_heading' is displayed
    And I hover over 'Modus_Site > jobs_link' and click element 'Modus_Site > jobs_link'
    And The title is 'Modus Create - Careers | Digital Transformation Consultants'
    And The element 'Modus_Site > Careers > dropdown_area' is displayed
    And The element 'Modus_Site > Careers > job_container' is displayed
    And I move to element 'Modus_Site > Careers > dropdown_area'
    And The element 'Modus_Site > Careers > job_container' is clickable
#    And I select the option 'All' by value for element 'Modus_Site > Careers > dropdown_filter'
    And I click item 'AHA Expert! (Product Manager)' for element 'Modus_Site > Careers > job_title'
    Then The page url contains 'com/careers/'
    When The element 'Modus_Site > Careers > main_iframe' is displayed
    And I switch to iframe 'Modus_Site > Careers > main_iframe'
    And I set text 'Tauqir' to field 'Modus_Site > Careers > first_name'
    And I set text 'Sarwar' to field 'Modus_Site > Careers > last_name'
    And I set text 'tauqir.sarwar@moduscreate.com' to field 'Modus_Site > Careers > email'
    And I set text '+921112563256' to field 'Modus_Site > Careers > phone'
    # locate me link does not work on safari - application issue
    And I click on button 'Modus_Site > Careers > location_link'
    When The element 'Modus_Site > Careers > resume_link' is displayed
    And I click on button 'Modus_Site > Careers > resume_link'
    And I set text 'testing resume' to field 'Modus_Site > Careers > resume_text'
    And I move to an element 'Modus_Site > Careers > move_form_dropdown' with offset '50' '200'
    And I click item 'Please select the country where you are living' for element 'Modus_Site > Careers > form_dropdown'
    And I click item 'Afghanistan' for element 'Modus_Site > Careers > country_dropdown'
    And I set text 'Modus Create' to field 'Modus_Site > Careers > current_company'
    And I set text 'QA Consultant' to field 'Modus_Site > Careers > current_title'
    And I click item 'Do you have a legal' for element 'Modus_Site > Careers > form_dropdown'
    And I click item 'Yes' for element 'Modus_Site > Careers > legal_dropdown'
    And I click item 'your consent in order' for element 'Modus_Site > Careers > form_dropdown'
    And I click item 'Yes' for element 'Modus_Site > Careers > consent_dropdown'
    And I click item 'work restricted' for element 'Modus_Site > Careers > form_dropdown'
    And I click item 'Yes' for element 'Modus_Site > Careers > restricted_dropdown'
    And I click item 'working for Modus as a Contract' for element 'Modus_Site > Careers > form_dropdown'
    And I click item 'Yes' for element 'Modus_Site > Careers > contract_dropdown'
    And I click item 'Modus before in any capacity' for element 'Modus_Site > Careers > form_dropdown'
    And I click item 'Yes' for element 'Modus_Site > Careers > capacity_dropdown'
    And I click item 'Please provide your salary expectations' for element 'Modus_Site > Careers > form_dropdown'
    And I click item '$12,000 - $12,500' for element 'Modus_Site > Careers > salary_dropdown'
    And I click item 'current notice period' for element 'Modus_Site > Careers > form_dropdown'
    And I click item '1-2 weeks' for element 'Modus_Site > Careers > notice_dropdown'
#    And I click item 'Contractor. Understanding' for element 'Modus_Site > Careers > form_dropdown'
    And I click item 'data protection apps upon hire' for element 'Modus_Site > Careers > form_dropdown'
    And I click item 'Yes' for element 'Modus_Site > Careers > position_dropdown'
#    And I click item 'Yes' for element 'Modus_Site > Careers > protection_dropdown'

  @gmail @automated @firefox @regression
  Scenario: Email Verification with email link
    Given I set web base url '{%BASE_URL%}'
    And Browser is maximized
    And The title is 'OrangeHRM'
    When The element 'OrangeHRM > username' is displayed
    And I set text '{%HRM_USER_NAME%}' to field 'OrangeHRM > username'
    And I set text '{%HRM_PASSWORD%}' to field 'OrangeHRM > password'
    And I click on element 'OrangeHRM > login_button'
    Then The title is 'OrangeHRM'
    And The page url contains 'dashboard'
    When I get link from email 'moduspytestboilerplate@gmail.com'