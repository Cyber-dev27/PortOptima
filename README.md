# PortOptima - Portfolio Optimizer using Genetic Algorithm

A professional Python GUI application for optimizing investment portfolios using a genetic algorithm approach to solve the constrained knapsack optimization problem.

## Features

### 📊 Portfolio Optimization

- **Genetic Algorithm-based Optimizer**: Uses evolutionary algorithms to find optimal portfolio compositions
- **Knapsack Optimization**: Maximizes expected returns while respecting risk constraints
- **Multi-stock Support**: Build portfolios from a library of 10+ real-world stocks

### 💼 Stock Management

- **Available Stocks Library**: Browse and manage a rich database of stocks
- **Stock Details**: View detailed information including:
  - Current price
  - Risk/Volatility metrics
  - Expected annual returns
  - Year-to-date performance
  - 12-month price history charts
- **Add/Remove Functionality**: Easily construct custom portfolios

### 📈 Performance Analysis

- **Performance Graphs**: Visual 12-month price history for any stock
- **Portfolio Metrics**: Comprehensive analysis including:
  - Total portfolio value
  - Total risk (combined volatility)
  - Expected returns
  - Sharpe ratio approximation
- **Visualizations**: Pie charts showing portfolio allocation and bar charts comparing risk vs. return

### 🧬 Genetic Algorithm Details

The optimizer implements a sophisticated genetic algorithm with:

- **Population size**: 100 individuals per generation
- **Generations**: Configurable (default 150)
- **Selection**: Tournament selection with 5-individual tournaments
- **Crossover**: Single-point crossover with 90% probability
- **Mutation**: Random bit-flip mutation with configurable rate (default 10%)
- **Fitness Function**: Maximizes expected returns with penalty for exceeding risk capacity
- **Constraints**: Respects user-defined risk budget/capacity


#### Visualizations:

- **Pie Chart**: Shows portfolio allocation by price
- **Bar Chart**: Compares risk and return metrics for each stock


### Problem Definition

The portfolio optimization problem is modeled as a **constrained 0/1 knapsack**:

- **Objective**: Maximize total expected return
- **Constraint**: Total portfolio risk ≤ risk capacity (budget)
- **Variables**: Include each stock (1) or exclude it (0)


### Performance Characteristics

- **Computation Time**: ~1-3 seconds for 10 stocks with 150 generations
- **Scalability**: Works well with up to 50-100 stocks; may need optimization for larger libraries


## Future Enhancements

- [ ] Real-time stock data integration (Yahoo Finance, Alpha Vantage)
- [ ] Portfolio rebalancing scheduler
- [ ] Multi-objective optimization (risk-return tradeoff)
- [ ] Constraint handling (sector limits, min/max positions)
- [ ] Backtesting functionality
- [ ] Risk factor analysis (VaR, CVaR)
- [ ] Export portfolio to CSV
- [ ] Save/load portfolio configurations


## Disclaimer

**This application is for educational and analytical purposes only. It is not financial advice. Always consult with a qualified financial advisor before making investment decisions.**


