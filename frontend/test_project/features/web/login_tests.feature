@nondestructive @web_tests
Feature:  OrangeHRM Login and Modus QA blog

    @hrm_login @hrm_logout @automated
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

    @hrm_add_user @automated
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
        When The element 'OrangeHRM > User > success_message' is displayed
        When The element 'OrangeHRM > User > add_button' is displayed
        And I set value 'Tauqir_Sarwar' for item 'Username' on element 'OrangeHRM > User > search_field'
        When I click on button 'OrangeHRM > User > search_button'
        Then I expect 'OrangeHRM > User > search_result' elements are present with innertext:
            | Tauqir_Sarwar |
            | ESS           |
        When I click on button 'OrangeHRM > User > delete_button'
        And I click on button 'OrangeHRM > User > delete_confirm'
        Then The element 'OrangeHRM > User > success_message' is displayed

    @blog_search @automated
    Scenario: Check QA modus blog
        Given I set web base url 'https://moduscreate.com'
        And The browser resolution is '1024' per '768'
        And The title is 'Modus Create | Consulting and Product Development Partner'
        When The element 'Modus_Site > main_heading' is displayed
        And I click item 'Blog' for element 'Modus_Site > header_link'
        And The title is 'Blog | Digital Transformation Insights - Modus Create'
        When The element 'Modus_Site > dropdown' is displayed
        And I select the option 'quality-assurance' by value for element 'Modus_Site > dropdown'
        And I pause for '5' s
        And I set text 'How to Avoid Flaky' to field 'Modus_Site > search_bar'
        When I click on button 'Modus_Site > search_icon'
        And The element 'Modus_Site > search_result' is displayed
        When I click on element 'Modus_Site > search_result'
        And The title is 'How to Avoid Flaky Tests? - Modus Create'
        And I scroll to element 'Modus_Site > blog_heading_1'
        And I scroll to element 'Modus_Site > blog_heading_2'
        And I scroll to element 'Modus_Site > blog_heading_1'
        And With soft assertion 'True' The element 'Modus_Site > sub_popup_close' is not displayed


    @sd_login @sd_login_error @sd_checkout @automated
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
        Then I expect that item '32.39' for element 'SourceDemo_Site > Checkout_page > total_amount' is displayed
        When I click on button 'SourceDemo_Site > Checkout_page > finish'
        And The element 'SourceDemo_Site > Checkout_page > thank_you_message' is displayed


    @sd_failure_message @automated
    Scenario: Try to login into saucedemo site with in-valid credentials
        Given I set web base url 'https://www.saucedemo.com'
        And Browser is maximized
        And The title is 'Swag Labs'
        When The element 'SourceDemo_Site > username' is displayed
        And I set text 'standard_user1' to field 'SourceDemo_Site > username'
        And I set text 'secret_sauce1' to field 'SourceDemo_Site > password'
        And I click on element 'SourceDemo_Site > login_button'
        Then The element 'SourceDemo_Site > login_error_message' is displayed
