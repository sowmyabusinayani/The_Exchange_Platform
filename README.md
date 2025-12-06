# 🌐 The Exchange Platform

A full-stack B2B order management system designed to handle complex inventory logistics and multi-stage trade flows. This project demonstrates a decoupled Frontend/Backend architecture, robust stock validation logic, and a reactive user interface.

---

## Project Overview
The Exchange Platform is a simulation of a specialized trading engine where inventory management goes beyond simple "In Stock / Out of Stock" binary states. 

It is designed to handle **Triangular Trade** scenarios where inventory must be tracked across two distinct states:
1.  **Available Stock:** Physical inventory currently on hand and ready for new sales.
2.  **Committed Stock:** Inventory that has been sold and reserved for a specific order but has not yet been shipped.

This distinction allows logistics teams to accurately plan shipments without overselling or losing track of reserved goods.

---

## Key Enhancements & Features (V2.0)

### 1. Dual-Status Inventory Logic
Refactored the core data model to support advanced logistics flows.
* **The Problem:** Traditional e-commerce systems often delete stock immediately upon sale, losing data on what is currently "in the warehouse" waiting for export.
* **The Solution:** Implemented a `committed_stock` attribute. When an order is placed, stock is moved from *Available* to *Committed* rather than being destroyed. This ensures accurate accounting for logistics and shipping departments.

### 2. Batch Order Processing (Cart System)
Upgraded the backend to handle bulk transactions.
* **Transactional Integrity:** The system processes lists of items as a single order event.
* **Atomic Validation:** If any single item in the bulk order exceeds available stock, the system intelligently flags the issue and prevents partial fulfillment errors.

### 3. Reactive Single Page Application (SPA)
A modern, responsive frontend interface built with Vanilla JavaScript and CSS3.
* **Dynamic Shop Interface:** Real-time rendering of product catalogs with visual stock indicators.
* **Interactive Cart:** Dynamic quantity adjustments that automatically respect backend inventory limits (e.g., users cannot select more items than are physically available).
* **RESTful Integration:** Seamless asynchronous communication with the Python/Flask backend using the Fetch API.

---

## Technical Architecture

### Backend
* **Framework:** Python (Flask)
* **Architecture Pattern:** MVC (Model-View-Controller) with REST API endpoints.
* **Data Models:** Object-Oriented design separating `Product`, `Customer`, and `Order` logic.
* **Logic Layer:** Encapsulated business rules ensure stock is never over-committed.

### Frontend
* **Core:** HTML5, CSS3, JavaScript (ES6+).
* **Design:** Custom responsive layout with glass-morphism UI elements and parallax hero sections.
* **State Management:** Client-side state handling for Cart management before API submission.

---

## Usage Workflow

1.  **Browse Catalog:** Users view available products with real-time pricing and stock data.
2.  **Add to Cart:** Users select items. The UI proactively limits quantity selection based on live `available_stock`.
3.  **Checkout:** The client sends a JSON payload to `POST /orders`.
4.  **Backend Processing:** The server validates availability, moves stock to "Committed" status, and returns a confirmation.

---

## Setup & Installation

1.  **Clone the Repository**
    ```
    git clone [https://github.com/sowmyabusinayani/The_Exchange_Platform.git]
    cd the-exchange-platform
    ```

2.  **Run the Application**
    ```
    python app.py
    ```

3.  **Launch**
    Open your browser and navigate to:
    `http://127.0.0.1:5000`

---

## 🔮 Future Roadmap
* **Persistence:** Integration with PostgreSQL for long-term historical data analysis.
* **Logistics Dashboard:** An Admin View to visualize the ratio of Available vs. Committed stock for shipping planning.
* **Containerization:** Docker support for cloud-native deployment.

---
*Developed by Sowmya Businayani*