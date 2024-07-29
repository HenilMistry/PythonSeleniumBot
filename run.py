from booking.booking import Booking

with Booking() as bot:
    bot.land_first_page()
    bot.check_for_signin_info()
    bot.change_currency("INR")
    bot.select_place_to_go("Surat")
    bot.select_dates(check_in_date="2024-08-01", check_out_date="2024-08-05")
    bot.select_adults(2)
    bot.click_search()
    bot.apply_alterations()
    print("Exiting...")
