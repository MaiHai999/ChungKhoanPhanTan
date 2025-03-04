# Stock Trading Management System Backend

## Overview
This is the backend service for the Stock Trading Management System, built using Flask and SQL Server. The system is designed to manage investor transactions at securities companies operating on the HNX (Hanoi Stock Exchange) and follows a distributed database model.

## Features
- **Investor Management:** Register and manage investor information.
- **Stock Management:** Manage stock listings, prices, and market regulations.
- **Order Management:** Process buy/sell orders, including different order types (LO, MB).
- **Transaction Matching:** Handle order execution and update order status.
- **Distributed Database:** Data is distributed across three servers:
  - `server1`: Contains securities company data and orders from company `010`.
  - `server2`: Contains securities company data and orders from company `020`.
  - `server3`: Central HNX server that stores all transactions.

## Tech Stack
- **Backend:** Flask (Python)
- **Database:** SQL Server, JOB, Stored Procedure, Trigger, Cursor
- **ORM:** SQLAlchemy
- **Authentication:** JWT (JSON Web Token)
- **API Documentation:** Swagger (Flask-Swagger)
