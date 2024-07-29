from booking.booking import Booking

try:
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

except Exception as e:
    if 'in PATH' in str(e):
        print("""
            You are trying to run the bot from the command line
            Please add to PATH your Selenium Drivers
            Windows:
                set PATH=%PATH%;<path-to-your-driver>
                
            Linux:
                PATH=$PATH:/<path-to-your-folder>
        """)
    else:
        raise
