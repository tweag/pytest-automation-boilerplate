@nondestructive @automated @android_mobile_tests
Feature: Basic App functionality

    Background: Login to the app
        Given I open the mobile application
        When The element 'Android > _mob > MyDemoApp > menu_icon' is displayed
        And I click on element 'Android > _mob > MyDemoApp > menu_icon'
        When The element 'Android > _mob > MyDemoApp > login' is displayed
        And I click on element 'Android > _mob > MyDemoApp > login'
        And The element 'Android > _mob > MyDemoApp > username' is displayed
        And I set text 'bob' to field 'Android > _mob > MyDemoApp > username'
        And I add text '@example.com' to field 'Android > _mob > MyDemoApp > username'
        And I set text '10203040' to field 'Android > _mob > MyDemoApp > password'
        And The element 'Android > _mob > MyDemoApp > login_button' is displayed
        And I click on element 'Android > _mob > MyDemoApp > login_button'
        When The element 'Android > _mob > MyDemoApp > menu_icon' is displayed
        And The element 'Android > _mob > MyDemoApp > menu_icon' is clickable

    @mobile_test @android
    Scenario: Verify logout from app on android app
        When I click on element 'Android > _mob > MyDemoApp > menu_icon'
        Then The element 'Android > _mob > MyDemoApp > logout' is displayed
        When I click on element 'Android > _mob > MyDemoApp > logout'
        Then The element 'Android > _mob > MyDemoApp > confirm_logout' is displayed
        When I click on element 'Android > _mob > MyDemoApp > confirm_logout'
        Then The element 'Android > _mob > MyDemoApp > logout_confirm_message' is displayed
        When I click on element 'Android > _mob > MyDemoApp > logout_confirm_message'
        Then The element 'Android > _mob > MyDemoApp > username' is displayed

    @mobile_test @android
    Scenario: Verify Add and Remove items from cart on android app
        When The element 'Android > _mob > MyDemoApp > item_sl_backpack' is displayed
        And I swipe down '50' % each time for '4' times
        And I click on element 'Android > _mob > an-items > Sauce_Labs_Onesie'
        And I swipe down '50' % each time for '1' times
        And The element 'Android > _mob > MyDemoApp > add_to_cart' is displayed
        And I click on element 'Android > _mob > MyDemoApp > add_to_cart'
        When I click on element 'Android > _mob > MyDemoApp > add_to_cart'
        Then The element 'Android > _mob > MyDemoApp > cart_badge_items' is displayed
        And The element 'Android > _mob > MyDemoApp > cart_badge_items' text is '2'
        When I click on element 'Android > _mob > MyDemoApp > cart_badge_items'
        And The element 'Android > _mob > MyDemoApp > my_cart_header' is displayed
        And I click on element 'Android > _mob > MyDemoApp > remove_item'
        And The element 'Android > _mob > MyDemoApp > Go_Shopping' is displayed
        And I click on element 'Android > _mob > MyDemoApp > Go_Shopping'
        Then The element 'Android > _mob > an-items > Sauce_Labs_Onesie' is displayed
        When I click on element 'Android > _mob > MyDemoApp > menu_icon'
        Then The element 'Android > _mob > MyDemoApp > logout' is displayed
        When I click on element 'Android > _mob > MyDemoApp > logout'
        Then The element 'Android > _mob > MyDemoApp > confirm_logout' is displayed
        When I click on element 'Android > _mob > MyDemoApp > confirm_logout'
        Then The element 'Android > _mob > MyDemoApp > logout_confirm_message' is displayed
        When I click on element 'Android > _mob > MyDemoApp > logout_confirm_message'
        Then The element 'Android > _mob > MyDemoApp > username' is displayed

    @mobile_test @android
    Scenario: Verify Place Order on android app
        When The element 'Android > _mob > MyDemoApp > item_sl_backpack' is displayed
        And I swipe down '50' % each time for '4' times
        And I click on element 'Android > _mob > an-items > Sauce_Labs_Onesie'
        And I swipe down '50' % each time for '1' times
        Then The element 'Android > _mob > MyDemoApp > add_to_cart' is displayed
        When I click on element 'Android > _mob > MyDemoApp > add_to_cart'
        And I click on element 'Android > _mob > MyDemoApp > add_to_cart'
        Then The element 'Android > _mob > MyDemoApp > cart_badge_items' is displayed
        When The element 'Android > _mob > MyDemoApp > cart_badge_items' text is '2'
        And I click on element 'Android > _mob > MyDemoApp > cart_badge_items'
        Then The element 'Android > _mob > MyDemoApp > my_cart_header' is displayed
        And The element 'Android > _mob > MyDemoApp > checkout' is displayed
        When I click on element 'Android > _mob > MyDemoApp > checkout'
        Then The element 'Android > _mob > an-Shipping_Info > Full_name' is displayed
        When I set text 'Tauqir Sarwar' to field 'Android > _mob > an-Shipping_Info > Full_name'
        And I set text 'Main Cantt' to field 'Android > _mob > an-Shipping_Info > Address_line_1'
        And I swipe down '50' % each time for '1' times
        And I set text 'Lahore' to field 'Android > _mob > an-Shipping_Info > City'
        And I swipe down '50' % each time for '2' times
        And I set text '102040' to field 'Android > _mob > an-Shipping_Info > Zip_code'
        And I set text 'Pakistan' to field 'Android > _mob > an-Shipping_Info > Country'
        And I swipe down '50' % each time for '1' times
        And I click on element 'Android > _mob > an-Payment_Detail > Payment'
        Then The element 'Android > _mob > an-Payment_Detail > Full_name' is displayed
        When I set text 'Tauqir Sarwar' to field 'Android > _mob > an-Payment_Detail > Full_name'
        And I swipe down '50' % each time for '1' times
        And I set text '325885556585999' to field 'Android > _mob > an-Payment_Detail > Card_Number'
        And I swipe down '50' % each time for '1' times
        And I set text '0325' to field 'Android > _mob > an-Payment_Detail > expired_card'
        And I set text '123' to field 'Android > _mob > an-Payment_Detail > CVV'
        And I swipe down '50' % each time for '1' times
        Then The element 'Android > _mob > an-Review_Order > Review' is displayed
        When I click on element 'Android > _mob > an-Review_Order > Review'
        And I swipe down '50' % each time for '2' times
        Then The element 'Android > _mob > an-Review_Order > Total' is displayed
        When I click on element 'Android > _mob > an-Review_Order > Place_Order'
        Then The element 'Android > _mob > an-Review_Order > Order_Complete' is displayed
