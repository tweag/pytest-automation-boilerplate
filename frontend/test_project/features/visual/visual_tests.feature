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
            | base_image                     |
            | mac-chrome-reset-pwd-page-full.png |

    @HRM_login_button @automated
    Scenario: Test the login button design
        When The element 'OrangeHRM > username' is displayed
        And The element 'OrangeHRM > username' is enabled
        And I pause for '5' s
        Then I verify that element 'OrangeHRM > login_button' is not visually regressed:
            | base_image                  |
            | mac-chrome-login-button.png |

