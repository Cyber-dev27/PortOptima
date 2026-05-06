import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random


class Stock:
    """Represents a stock with price and performance data."""
    def __init__(self, symbol, name, price, risk, expected_return, base_price=100):
        self.symbol = symbol
        self.name = name
        self.price = price
        self.risk = risk
        self.expected_return = expected_return
        self.historical_prices = self._generate_historical_prices(base_price)
        
    def _generate_historical_prices(self, base):
        """Generate realistic historical price data."""
        prices = [base]
        for _ in range(364):
            daily_return = np.random.normal(self.expected_return / 365, self.risk / np.sqrt(252))
            prices.append(prices[-1] * (1 + daily_return))
        return prices
    
    def get_performance(self):
        """Calculate YTD performance percentage."""
        if len(self.historical_prices) < 2:
            return 0.0
        return ((self.historical_prices[-1] - self.historical_prices[0]) / 
                self.historical_prices[0] * 100)


class GeneticAlgorithmOptimizer:
    """Genetic Algorithm for portfolio optimization."""
    def __init__(self, population_size=100, generations=150, mutation_rate=0.1, crossover_rate=0.9):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
    
    def optimize(self, weights, values, capacity, budget=None):
        """Optimize portfolio using genetic algorithm with risk and budget constraints."""
        num_items = len(weights)
        population = self._create_initial_population(num_items)
        best_solution = None
        best_fitness = float('-inf')
        
        for generation in range(self.generations):
            fitness_scores = []
            for individual in population:
                fitness, weight = self._evaluate_fitness(individual, weights, values, capacity, budget)
                fitness_scores.append((individual, fitness, weight))
                
                if fitness > best_fitness:
                    best_fitness = fitness
                    best_solution = individual.copy()
                    best_weight = weight
            
            new_population = []
            for _ in range(self.population_size):
                parent1 = self._tournament_selection(fitness_scores)
                parent2 = self._tournament_selection(fitness_scores)
                
                if random.random() < self.crossover_rate:
                    child1, child2 = self._crossover(parent1[0], parent2[0])
                else:
                    child1, child2 = parent1[0].copy(), parent2[0].copy()
                
                child1 = self._mutate(child1)
                child2 = self._mutate(child2)
                new_population.extend([child1, child2])
            
            population = new_population[:self.population_size]
        
        solution_indices = [i for i, gene in enumerate(best_solution) if gene == 1]
        return solution_indices, best_fitness, best_weight
    
    def _create_initial_population(self, num_items):
        return [[random.randint(0, 1) for _ in range(num_items)] for _ in range(self.population_size)]
    
    def _evaluate_fitness(self, individual, weights, values, capacity, budget=None):
        total_value = sum(v for i, v in enumerate(values) if individual[i] == 1)
        total_weight = sum(w for i, w in enumerate(weights) if individual[i] == 1)
        total_price = sum(individual[i] * self.stock_prices[i] for i in range(len(individual))) if hasattr(self, 'stock_prices') and budget is not None else 0
        
        # Penalty for exceeding risk capacity
        if total_weight > capacity:
            total_value -= (total_weight - capacity) * 100
        
        # Penalty for exceeding budget
        if budget is not None and total_price > budget:
            total_value -= (total_price - budget) * 50
        
        return total_value, total_weight
    
    def _tournament_selection(self, fitness_scores):
        tournament = random.sample(fitness_scores, min(5, len(fitness_scores)))
        return max(tournament, key=lambda x: x[1])
    
    def _crossover(self, parent1, parent2):
        point = random.randint(1, len(parent1) - 1)
        return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]
    
    def _mutate(self, individual):
        for i in range(len(individual)):
            if random.random() < self.mutation_rate:
                individual[i] = 1 - individual[i]
        return individual


class PortOptima(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PortOptima - Portfolio Optimizer with Genetic Algorithm")
        self.geometry("1200x700")
        
        # Create sample stocks
        self.available_stocks = self._create_sample_stocks()
        self.portfolio_stocks = []
        self.optimizer = GeneticAlgorithmOptimizer(population_size=100, generations=100)
        
        self.setup_ui()
    
    def _create_sample_stocks(self):
        configs = [
            {"symbol": "TCS", "name": "Tata Consultancy Services", "price": 3950.00, "risk": 0.22, "return": 0.15},
            {"symbol": "INFY", "name": "Infosys Ltd.", "price": 1850.75, "risk": 0.18, "return": 0.18},
            {"symbol": "RELIANCE", "name": "Reliance Industries", "price": 2750.50, "risk": 0.20, "return": 0.16},
            {"symbol": "HDFCBANK", "name": "HDFC Bank Ltd.", "price": 1950.25, "risk": 0.25, "return": 0.14},
            {"symbol": "ITC", "name": "ITC Limited", "price": 455.30, "risk": 0.30, "return": 0.20},
            {"symbol": "MARUTI", "name": "Maruti Suzuki India", "price": 10850.00, "risk": 0.28, "return": 0.17},
            {"symbol": "BAJAJFINSV", "name": "Bajaj Finserv Ltd.", "price": 16200.50, "risk": 0.32, "return": 0.25},
            {"symbol": "LT", "name": "Larsen & Toubro", "price": 2950.75, "risk": 0.15, "return": 0.12},
            {"symbol": "HCLTECH", "name": "HCL Technologies", "price": 1680.25, "risk": 0.16, "return": 0.14},
            {"symbol": "WIPRO", "name": "Wipro Limited", "price": 420.50, "risk": 0.12, "return": 0.10},
        ]
        return [Stock(c["symbol"], c["name"], c["price"], c["risk"], c["return"], c["price"] * 0.8) 
                for c in configs]
    
    def setup_ui(self):
        """Setup user interface."""
        # Main frames
        left_frame = ttk.Frame(self)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        right_frame = ttk.Frame(self)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ===== LEFT PANEL: AVAILABLE STOCKS =====
        ttk.Label(left_frame, text="Available Stocks", font=("Arial", 12, "bold")).pack()
        
        # Stocks table
        self.stocks_tree = ttk.Treeview(left_frame, columns=("Name", "Price", "Risk", "Return"), height=10)
        self.stocks_tree.column("#0", width=60, anchor="center")
        self.stocks_tree.column("Name", width=150, anchor="w")
        self.stocks_tree.column("Price", width=80, anchor="center")
        self.stocks_tree.column("Risk", width=70, anchor="center")
        self.stocks_tree.column("Return", width=80, anchor="center")
        
        self.stocks_tree.heading("#0", text="Symbol")
        self.stocks_tree.heading("Name", text="Name")
        self.stocks_tree.heading("Price", text="Price")
        self.stocks_tree.heading("Risk", text="Risk")
        self.stocks_tree.heading("Return", text="Return")
        
        for stock in self.available_stocks:
            self.stocks_tree.insert("", "end", text=stock.symbol, values=(
                stock.name, f"₹{stock.price:.2f}", f"{stock.risk:.1%}", f"{stock.expected_return:.1%}"
            ))
        
        self.stocks_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Add to Portfolio →", command=self.add_to_portfolio).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="View Details", command=self.view_stock_details).pack(side=tk.LEFT, padx=2)
        
        # ===== RIGHT PANEL: PORTFOLIO & OPTIMIZATION =====
        ttk.Label(right_frame, text="My Portfolio", font=("Arial", 12, "bold")).pack()
        
        # Portfolio table
        self.portfolio_tree = ttk.Treeview(right_frame, columns=("Name", "Price", "Risk", "Return"), height=8)
        self.portfolio_tree.column("#0", width=60, anchor="center")
        self.portfolio_tree.column("Name", width=150, anchor="w")
        self.portfolio_tree.column("Price", width=80, anchor="center")
        self.portfolio_tree.column("Risk", width=70, anchor="center")
        self.portfolio_tree.column("Return", width=80, anchor="center")
        
        self.portfolio_tree.heading("#0", text="Symbol")
        self.portfolio_tree.heading("Name", text="Name")
        self.portfolio_tree.heading("Price", text="Price")
        self.portfolio_tree.heading("Risk", text="Risk")
        self.portfolio_tree.heading("Return", text="Return")
        
        self.portfolio_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Portfolio buttons
        btn_frame2 = ttk.Frame(right_frame)
        btn_frame2.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame2, text="Remove Selected", command=self.remove_from_portfolio).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame2, text="Clear Portfolio", command=self.clear_portfolio).pack(side=tk.LEFT, padx=2)
        
        # Optimization parameters
        params_frame = ttk.LabelFrame(right_frame, text="Optimization Settings", padding=10)
        params_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(params_frame, text="Risk Capacity:").grid(row=0, column=0, sticky="w")
        self.risk_capacity = tk.DoubleVar(value=1.5)
        risk_spin = ttk.Spinbox(params_frame, from_=0.1, to=5.0, textvariable=self.risk_capacity, width=10)
        risk_spin.grid(row=0, column=1, sticky="w", padx=5)
        
        ttk.Label(params_frame, text="Budget (₹):").grid(row=1, column=0, sticky="w")
        self.budget = tk.DoubleVar(value=150000.0)
        budget_spin = ttk.Spinbox(params_frame, from_=10000, to=5000000, textvariable=self.budget, width=10)
        budget_spin.grid(row=1, column=1, sticky="w", padx=5)
        
        # Optimize button
        ttk.Button(right_frame, text="🧬 Optimize Portfolio", command=self.optimize).pack(fill=tk.X, pady=10)
        
        # Results text area
        ttk.Label(right_frame, text="Results", font=("Arial", 10, "bold")).pack()
        self.results_text = scrolledtext.ScrolledText(right_frame, height=10, width=50)
        self.results_text.pack(fill=tk.BOTH, expand=True, pady=5)
    
    def add_to_portfolio(self):
        """Add selected stock to portfolio."""
        selected = self.stocks_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a stock to add.")
            return
        
        symbol = self.stocks_tree.item(selected[0], "text")
        stock = next((s for s in self.available_stocks if s.symbol == symbol), None)
        
        if stock and stock not in self.portfolio_stocks:
            self.portfolio_stocks.append(stock)
            self.update_portfolio_tree()
            messagebox.showinfo("Success", f"{symbol} added to portfolio!")
    
    def remove_from_portfolio(self):
        """Remove selected stock from portfolio."""
        selected = self.portfolio_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a stock to remove.")
            return
        
        symbol = self.portfolio_tree.item(selected[0], "text")
        self.portfolio_stocks = [s for s in self.portfolio_stocks if s.symbol != symbol]
        self.update_portfolio_tree()
    
    def clear_portfolio(self):
        """Clear entire portfolio."""
        self.portfolio_stocks.clear()
        self.update_portfolio_tree()
    
    def update_portfolio_tree(self):
        """Update portfolio table display."""
        for item in self.portfolio_tree.get_children():
            self.portfolio_tree.delete(item)
        
        for stock in self.portfolio_stocks:
            self.portfolio_tree.insert("", "end", text=stock.symbol, values=(
                stock.name, f"₹{stock.price:.2f}", f"{stock.risk:.1%}", f"{stock.expected_return:.1%}"
            ))
    
    def view_stock_details(self):
        """Show stock details window with chart."""
        selected = self.stocks_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a stock.")
            return
        
        symbol = self.stocks_tree.item(selected[0], "text")
        stock = next((s for s in self.available_stocks if s.symbol == symbol), None)
        
        if not stock:
            return
        
        # Create details window
        details_window = tk.Toplevel(self)
        details_window.title(f"{stock.symbol} - {stock.name}")
        details_window.geometry("700x500")
        
        # Info
        info_text = f"Price: ₹{stock.price:.2f} | Risk: {stock.risk:.1%} | Return: {stock.expected_return:.1%} | Performance: {stock.get_performance():.2f}%"
        ttk.Label(details_window, text=info_text, font=("Arial", 10)).pack(padx=10, pady=10)
        
        # Chart
        fig = Figure(figsize=(7, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(stock.historical_prices, linewidth=2, color='blue')
        ax.fill_between(range(len(stock.historical_prices)), stock.historical_prices, alpha=0.3)
        ax.set_title(f"{stock.symbol} - 12 Month Price History")
        ax.set_xlabel("Days")
        ax.set_ylabel("Price (₹)")
        ax.grid(True, alpha=0.3)
        
        canvas = FigureCanvasTkAgg(fig, master=details_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def optimize(self):
        """Run genetic algorithm optimization."""
        if not self.portfolio_stocks:
            messagebox.showwarning("Empty Portfolio", "Add stocks to portfolio before optimizing.")
            return
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Optimizing... Please wait...\n")
        self.update()
        
        try:
            weights = [s.risk for s in self.portfolio_stocks]
            values = [s.expected_return for s in self.portfolio_stocks]
            capacity = self.risk_capacity.get()
            budget = self.budget.get()
            
            self.optimizer.stock_prices = [s.price for s in self.portfolio_stocks]
            optimal_indices, best_fitness, best_weight = self.optimizer.optimize(weights, values, capacity, budget)
            
            optimal_stocks = [self.portfolio_stocks[i] for i in optimal_indices]
            
            total_price = sum(self.portfolio_stocks[i].price for i in optimal_indices)
            total_risk = sum(self.portfolio_stocks[i].risk for i in optimal_indices)
            total_return = sum(self.portfolio_stocks[i].expected_return for i in optimal_indices)
            budget_used = (total_price / budget * 100) if budget > 0 else 0
            
            # Display results
            self.results_text.delete(1.0, tk.END)
            results = f"""
=== OPTIMIZATION RESULTS ===
Selected Stocks: {len(optimal_indices)}
Portfolio Value: ₹{total_price:.2f}
Budget Limit: ₹{budget:.2f}
Budget Used: {budget_used:.1f}%
Total Risk: {total_risk:.4f}
Total Return: {total_return:.2%}
Sharpe Ratio: {(total_return/total_risk if total_risk > 0 else 0):.4f}
Fitness Score: {best_fitness:.2f}

COMPOSITION:
"""
            for stock in optimal_stocks:
                results += f"\n✓ {stock.symbol}: {stock.name}\n   Price: ₹{stock.price:.2f} | Risk: {stock.risk:.1%}"
            
            self.results_text.insert(tk.END, results)
            
            # Show visualization
            self.show_results_chart(optimal_stocks, budget, total_price)
            
        except Exception as e:
            messagebox.showerror("Error", f"Optimization failed: {str(e)}")
    
    def show_results_chart(self, optimal_stocks, budget=None, total_price=None):
        """Show results visualization with budget allocation."""
        if not optimal_stocks:
            return
        
        chart_window = tk.Toplevel(self)
        chart_window.title("Portfolio Analysis")
        chart_window.geometry("1000x600")
        
        fig = Figure(figsize=(10, 6), dpi=100)
        
        # Pie chart of portfolio allocation
        ax1 = fig.add_subplot(221)
        symbols = [s.symbol for s in optimal_stocks]
        prices = [s.price for s in optimal_stocks]
        ax1.pie(prices, labels=symbols, autopct='%1.1f%%', startangle=90)
        ax1.set_title("Portfolio Allocation by Price")
        
        # Risk vs Return bar chart
        ax2 = fig.add_subplot(222)
        risks = [s.risk * 100 for s in optimal_stocks]
        returns = [s.expected_return * 100 for s in optimal_stocks]
        x = np.arange(len(symbols))
        width = 0.35
        ax2.bar(x - width/2, risks, width, label='Risk', alpha=0.8)
        ax2.bar(x + width/2, returns, width, label='Return', alpha=0.8)
        ax2.set_xlabel("Stock")
        ax2.set_ylabel("Percentage (%)")
        ax2.set_title("Risk vs Return Comparison")
        ax2.set_xticks(x)
        ax2.set_xticklabels(symbols, rotation=45)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Budget allocation pie chart
        if budget is not None and total_price is not None:
            ax3 = fig.add_subplot(223)
            remaining_budget = max(0, budget - total_price)
            budget_labels = ['Portfolio\nInvested', 'Remaining\nBudget']
            budget_values = [total_price, remaining_budget]
            colors = ['#2ecc71', '#e74c3c'] if remaining_budget >= 0 else ['#c0392b']
            ax3.pie(budget_values, labels=budget_labels, autopct='%1.1f%%', colors=colors, startangle=90)
            ax3.set_title(f"Budget Utilization (₹{budget:.0f})")
        
        # Stock prices table
        ax4 = fig.add_subplot(224)
        ax4.axis('tight')
        ax4.axis('off')
        table_data = [[s.symbol, f"₹{s.price:.2f}", f"{s.risk:.1%}", f"{s.expected_return:.1%}"] 
                      for s in optimal_stocks]
        table_data.insert(0, ['Symbol', 'Price', 'Risk', 'Return'])
        table = ax4.table(cellText=table_data, cellLoc='center', loc='center', 
                         colWidths=[0.2, 0.2, 0.2, 0.2])
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 1.8)
        ax4.set_title("Stock Details", pad=20)
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


if __name__ == "__main__":
    app = PortOptima()
    app.mainloop()
