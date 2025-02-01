# python find S&P 500 

# S&P 500

S&P 500, which has recorded the performance of the U.S. stock market since 1957 and covers 500 common stocks, is one of the most closely watched stock indices

## Features
- **Modern UI**: Responsive and visually appealing design.
- **Project Showcase**: Displays my latest work with images and descriptions.
- **Category Filtering**: Allows filtering projects by category.
- **Smooth Animations**: Powered by AOS (Animate On Scroll).
- **Deployed on Firebase Hosting**.

## Tech Stack
- **Frontend**: html
- **Backend**:python (flask backend)
- **Deployment**: Firebase Hosting

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yo-yo0613/python-flask-stock-search.git
   cd s-p500
   ```

2. Install dependencies:
   ```sh
   pip install flask yfinance pandas warnings time matplotlib seaborn plotly
   ```

3. Run the development server:
   ```sh
   python check.py
   ```

4. Open in browser: `http://127.0.0.1:5000/chart?ticker=AAPL`


## Folder Structure
```
my-portfolio/
├── public/           # Static assets (images, favicon, etc.)
├── src/
│   ├── assets/       # Local assets (logos, icons, etc.)
│   ├── components/   # Vue components
│   ├── views/        # Page views
│   ├── App.vue       # Main Vue app component
│   ├── main.js       # Entry file
├── dist/             # Production build output
├── firebase.json     # Firebase hosting configuration
├── vite.config.js    # Vite configuration
└── README.md         # Project documentation
```

## Known Issues
- Use String instead of https://en.wikipedia.org/wiki/List_of_S%26P_500_companies in your project data.
- You can search your stock in python terminal

## Contact
For any inquiries or suggestions, feel free to reach out!

---
Made with ❤️ using Vue.js and Vite.

