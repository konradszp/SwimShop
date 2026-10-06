from repositories import ProductRepository
from gui.views.login import LoginWindow
from gui.views.main_win import MainWindow



def main():
    def on_successful_login(user):
        point_of_sale = MainWindow(current_user=user, on_logout=main)
        point_of_sale.mainloop()

        
    app = LoginWindow(on_login_success=on_successful_login)
    app.mainloop()


if __name__ == "__main__":
    main()