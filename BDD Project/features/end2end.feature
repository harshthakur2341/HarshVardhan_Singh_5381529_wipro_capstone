Feature: End-to-End Train Ticket Booking Workflow

  @e2e_train
  Scenario: Successfully search, select, and enter payment details for a train ticket
    Given User launches MakeMyTrip application
    And User loads test data from Excel "test_data.xlsx"
    When User closes the login popup
    And User navigates to the Trains section
    Then the train search dashboard should be visible
    When User enters source station from Excel
    And User enters destination station from Excel
    And User selects a travel date
    And User selects the class type
    And User clicks on Search Trains button
    Then the train listing results page should be loaded
    When User applies the AC and Available filters
    And User selects the first available train ticket
    Then the specific train details page should be loaded
    When User opens the add traveller modal and enters passenger details from Excel
    And User enters IRCTC username from Excel
    And User fills contact details from Excel
    And User selects cancellation insurance and accepts mandatory terms
    And User proceeds to payment
    Then the payment page should be loaded and credit card option selected
    When User enters credit card details from Excel
    Then the payment continue button should become active