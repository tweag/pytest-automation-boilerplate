@nondestructive @visual
Feature:  OrangeHRM Visual Tests

    Background:
        Given I am on the page '/'
        And The browser resolution is '1024' per '768'
        And The title is 'OrangeHRM'

    @HRM_reset_page @automated
    Scenario: Test the Reset Password page design
        When The element 'OrangeHRM > reset_password' is displayed
        When I click on element 'OrangeHRM > reset_password'
        And The title is 'OrangeHRM'
        And The element 'OrangeHRM > username' is displayed
        Then I verify the page is not visually regressed:
            | base_image                         |
            | mac-chrome-reset-pwd-page-full.png |

    @HRM_login_button @automated
    Scenario: Test the login button design
        When The element 'OrangeHRM > username' is displayed
        And The element 'OrangeHRM > username' is enabled
        And I pause for '5' s
        Then I verify that element 'OrangeHRM > login_button' is not visually regressed:
            | base_image                  |
            | mac-chrome-login-button.png |


    @blog @automated
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
#        And The element 'Modus_Site > sub_popup_close' is displayed
#        When I click on button 'Modus_Site > sub_popup_close'
        Then I verify the page is not visually regressed:
            | base_image                    |
            | mac-chrome-blog-page-full.png |

