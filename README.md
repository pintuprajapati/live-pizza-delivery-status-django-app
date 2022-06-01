# live-pizza-delivery-status-django-app
Live delivery status will be shown to customer


![pizza_frontpage](https://user-images.githubusercontent.com/37404377/171337738-2e2350fd-79ae-46ad-894e-7d9f59ada71d.jpg)
![pizza_backend](https://user-images.githubusercontent.com/37404377/171337743-d8ecfcaa-999e-4259-b5df-e2c9b1ce6a19.jpg)

To run this project in your local system, follow below steps: 

1. Clone the project
2. Run the project by typing this command:
   `python manage.py runserver`
3. First login to admin panel:
   go to `http://127.0.0.1:8000/admin/`
   -  username: admin
   - password: 123
4. Now try to run the home page:
    go to `http://127.0.0.1:8000/`
    - Click on 'View' on any pizza item -> Remember the 'Order Id'
    - Open the 'admin panel' -> go to 'Orders' -> Choose same 'Order Id' as shown on home page
    - Now change the status of delivery
    - It will automatically change the status of delivery on front page to the user

Features of the site:
- Customer won't have to refresh the page to see the status of delivery of his pizza
- It is automatically handled by Django Channels in backend.
