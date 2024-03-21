@nondestructive @automated @ios_mobile_tests
Feature: Basic IOS App functionality

    @mobile_test @ios
    Scenario: Verify login/logout on IOS app
        Given I open the mobile application
        When The element '_mob > MyDemoApp > Catalog' is displayed
        And I click on element '_mob > MyDemoApp > Catalog'
        And The element '_mob > MyDemoApp > Cart_Icon' is displayed
        And I click on element '_mob > MyDemoApp > Cart_Icon'
        And The element '_mob > MyDemoApp > Go_Shopping' is displayed
        And I click on element '_mob > MyDemoApp > Go_Shopping'
        And The element '_mob > MyDemoApp > item_sl_backpack' is displayed
        And I click on element '_mob > MyDemoApp > menu_icon'
        And The element '_mob > MyDemoApp > login' is displayed
        And I click on element '_mob > MyDemoApp > login'
        And The element '_mob > MyDemoApp > username' is displayed
        And I set text 'bob' to field '_mob > MyDemoApp > username'
        And I add text '@example.com' to field '_mob > MyDemoApp > username'
        And I set text '10203040' to field '_mob > MyDemoApp > password'
        And I click on element '_mob > MyDemoApp > login_button'
        When The element '_mob > MyDemoApp > Catalog' is displayed
        And The element '_mob > MyDemoApp > item_sl_backpack' is displayed
        And I click on element '_mob > MyDemoApp > menu_icon'
        And The element '_mob > MyDemoApp > logout' is displayed
        And I click on element '_mob > MyDemoApp > logout'
        And The element '_mob > MyDemoApp > confirm_logout' is displayed
        And I click on element '_mob > MyDemoApp > confirm_logout'
        And The element '_mob > MyDemoApp > logout_confirm_message' is displayed
        And I click on element '_mob > MyDemoApp > logout_confirm_message'
        And The element '_mob > MyDemoApp > username' is displayed

    @mobile_test @ios
    Scenario: Verify Add/Remove items from cart on IOS app
        Given I open the mobile application
        When The element '_mob > MyDemoApp > menu_icon' is displayed
        And I click on element '_mob > MyDemoApp > menu_icon'
        And The element '_mob > MyDemoApp > login' is displayed
        And I click on element '_mob > MyDemoApp > login'
        And The element '_mob > MyDemoApp > username' is displayed
        And I set text 'bob' to field '_mob > MyDemoApp > username'
        And I add text '@example.com' to field '_mob > MyDemoApp > username'
        And I set text '10203040' to field '_mob > MyDemoApp > password'
        And I click on element '_mob > MyDemoApp > login_button'
        When The element '_mob > MyDemoApp > item_sl_backpack' is displayed
        And I scroll to element '_mob > items > Sauce Labs Onesie' for '2' iterations
        And I click on element '_mob > items > Sauce Labs Onesie'
        And The element '_mob > MyDemoApp > add_to_cart' is displayed
        And I click on element '_mob > MyDemoApp > add_to_cart'
        And I click on element '_mob > MyDemoApp > add_to_cart'
        And The element '_mob > MyDemoApp > cart_badge_2_items' is displayed
        And I click on element '_mob > MyDemoApp > cart_badge_2_items'
        And The element '_mob > MyDemoApp > my_cart_header' is displayed
        And I click on element '_mob > MyDemoApp > remove_item'
        And The element '_mob > MyDemoApp > Go_Shopping' is displayed
        And I click on element '_mob > MyDemoApp > menu_icon'
        And The element '_mob > MyDemoApp > logout' is displayed
        And I click on element '_mob > MyDemoApp > logout'
        And The element '_mob > MyDemoApp > confirm_logout' is displayed
        And I click on element '_mob > MyDemoApp > confirm_logout'
        And The element '_mob > MyDemoApp > logout_confirm_message' is displayed
        And I click on element '_mob > MyDemoApp > logout_confirm_message'
        And The element '_mob > MyDemoApp > username' is displayed

    @mobile_test @ios
    Scenario: Verify Place Order on IOS app
        Given I open the mobile application
        When The element '_mob > MyDemoApp > menu_icon' is displayed
        And I click on element '_mob > MyDemoApp > menu_icon'
        And The element '_mob > MyDemoApp > login' is displayed
        And I click on element '_mob > MyDemoApp > login'
        And The element '_mob > MyDemoApp > username' is displayed
        And I set text 'bob' to field '_mob > MyDemoApp > username'
        And I add text '@example.com' to field '_mob > MyDemoApp > username'
        And I set text '10203040' to field '_mob > MyDemoApp > password'
        And I click on element '_mob > MyDemoApp > login_button'
        When The element '_mob > MyDemoApp > item_sl_backpack' is displayed
        And I scroll to element '_mob > items > Sauce Labs Onesie' for '2' iterations
        And I click on element '_mob > items > Sauce Labs Onesie'
        And The element '_mob > MyDemoApp > add_to_cart' is displayed
        And I click on element '_mob > MyDemoApp > add_to_cart'
        And I click on element '_mob > MyDemoApp > add_to_cart'
        And The element '_mob > MyDemoApp > cart_badge_2_items' is displayed
        And I click on element '_mob > MyDemoApp > cart_badge_2_items'
        And The element '_mob > MyDemoApp > checkout' is displayed
        And I click on element '_mob > MyDemoApp > checkout'
        And The element '_mob > Shipping_Info > Full_name' is displayed
        And I set text 'Tauqir Sarwar' to field '_mob > Shipping_Info > Full_name'
        And I set text 'Main Cantt' to field '_mob > Shipping_Info > Address_line_1'
        And I set text 'Lahore' to field '_mob > Shipping_Info > City'
        And I scroll to element '_mob > Shipping_Info > Zip_code' for '2' iterations
        And I set text '102040' to field '_mob > Shipping_Info > Zip_code'
        And I set text 'Pakistan' to field '_mob > Shipping_Info > Country'
        And I click on element '_mob > MyDemoApp > back_button'
        And I click on element '_mob > Payment_Detail > Payment'
        And The element '_mob > Payment_Detail > Full_name' is displayed
        And I set text 'Tauqir Sarwar' to field '_mob > Payment_Detail > Full_name'
        And I set text '325885556585999' to field '_mob > Payment_Detail > Card_Number'
        And I set text '0325' to field '_mob > Payment_Detail > expired_card'
        And I set text '123' to field '_mob > Payment_Detail > CVV'
        And I click on element '_mob > Payment_Detail > Enter_Click'
        And I click on element '_mob > Review_Order > Review'
        And I click on element '_mob > Review_Order > Review'
        And The element '_mob > Review_Order > Total' is displayed
        And I click on element '_mob > Review_Order > Place_Order'
        And The element '_mob > Review_Order > Order_Complete' is displayed
