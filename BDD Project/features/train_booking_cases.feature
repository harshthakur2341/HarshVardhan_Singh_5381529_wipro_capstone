Feature: Train Search and Booking Functionality Validations

  Background:
    Given User launches MakeMyTrip application
    When User closes the login popup
    And User navigates to the Trains section

  # POSITIVE TESTS
  @positive @search
  Scenario: Verify train search functionality using valid source and destination stations
    Given User extracts test data from CSV "train_search_data.csv" for row "1"
    When User provides search source station from CSV
    And User provides search destination station from CSV
    And User selects a travel date
    And User clicks on Search Trains button
    Then User should see the train search results successfully

  @positive @search @listing
  Scenario: Validate that the train listing page displays available trains after successful search
    Given User extracts test data from CSV "train_search_data.csv" for row "1"
    When User provides search source station from CSV
    And User provides search destination station from CSV
    And User selects a travel date
    And User clicks on Search Trains button
    Then User should see available trains listed on the results page

  @positive @search @filter
  Scenario: Verify train filters functionality using availability and class filters
    Given User extracts test data from CSV "train_search_data.csv" for row "1"
    When User provides search source station from CSV
    And User provides search destination station from CSV
    And User selects a travel date
    And User clicks on Search Trains button
    And User applies the AC and Available filters
    Then Verify that the train results update successfully based on filters

  @positive @booking @payment
  Scenario: Verify successful navigation to the payment page after passenger detail submission
    Given User extracts test data from CSV "train_search_data.csv" for row "1"
    When User provides search source station from CSV
    And User provides search destination station from CSV
    And User selects a travel date
    And User clicks on Search Trains button
    And User selects the first available train ticket
    And User opens the add traveller modal and enters passenger details from CSV
    And User enters IRCTC username from CSV
    And User fills contact details from CSV
    And User selects cancellation insurance and accepts mandatory terms
    And User proceeds to payment
    Then User should successfully navigate to the payment page

  # NEGATIVE TESTS
  @negative @search
  Scenario: Validate application behavior when the same source and destination stations are entered
    Given User extracts test data from CSV "negative_train_data.csv" for row "1"
    When User provides search source station from CSV
    And User provides search destination station from CSV
    And User clicks on Search Trains button
    Then User should see an error message stating stations cannot be the same

  @negative @booking @validation
  Scenario: Verify validation when invalid phone number is entered in passenger details
    Given User extracts test data from CSV "invalid_contact_data.csv" for row "1"
    When User provides search source station from CSV
    And User provides search destination station from CSV
    And User selects a travel date
    And User clicks on Search Trains button
    And User selects the first available train ticket
    And User opens the add traveller modal and enters passenger details from CSV
    And User enters IRCTC username from CSV
    And User selects cancellation insurance and accepts mandatory terms
    And User fills contact details with an invalid mobile number from CSV
    And User proceeds to payment
    Then User should see a validation error for the invalid mobile number