import { useEffect, useState } from "react";

import {
  DollarSign,
  ShoppingCart,
  Users,
  Package,
  Star,
  CreditCard,
  Tag,
  Store,
  Wallet,
} from "lucide-react";

import StatCard from "../components/StatCard";
import ChartCard from "../components/ChartCard";
import DataTable from "../components/DataTable";
import Loader from "../components/Loader";

import {
  getKPIs,
  getRecentOrders,
  getCurrentTopCategories,
} from "../services/api";

const formatCurrency = (value) => {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(value);
};

function CurrentDashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Load all dashboard sections together
    Promise.all([getKPIs(), getRecentOrders(), getCurrentTopCategories()])
      .then(([kpis, recentOrders, topCategories]) => {
        // Keep the API results together for the dashboard
        setDashboardData({
          kpis,
          recent_orders: recentOrders,
          top_categories: topCategories,
        });
      })
      .catch(() => {
        setError("Failed to load dashboard data.");
      });
  }, []);

  if (error) {
    return <p className="text-sm text-rose-600">{error}</p>;
  }

  if (!dashboardData) {
    return <Loader label="Loading dashboard data..." />;
  }

  const { kpis, recent_orders, top_categories } = dashboardData;

  const statCards = [
    {
      label: "Total Revenue",
      value: formatCurrency(kpis.total_revenue),
      icon: DollarSign,
      accent: "primary",
    },
    {
      label: "Total Orders",
      value: kpis.total_orders.toLocaleString(),
      icon: ShoppingCart,
      accent: "green",
    },
    {
      label: "Total Customers",
      value: kpis.total_customers.toLocaleString(),
      icon: Users,
      accent: "amber",
    },
    {
      label: "Total Products",
      value: kpis.total_products.toLocaleString(),
      icon: Package,
      accent: "rose",
    },
    {
      label: "Average Review",
      value: `${kpis.avg_review_score} / 5`,
      icon: Star,
      accent: "primary",
    },
    {
      label: "Average Payment",
      value: formatCurrency(kpis.avg_payment_value),
      icon: Wallet,
      accent: "green",
    },
    {
      label: "Top Category",
      value: kpis.top_selling_category,
      icon: Tag,
      accent: "amber",
    },
    {
      label: "Top Seller",
      value: kpis.top_seller,
      icon: Store,
      accent: "rose",
    },
    {
      label: "Payment Method",
      value: kpis.top_payment_method,
      icon: CreditCard,
      accent: "primary",
    },
  ];

  return (
    <div className="fade-in space-y-4">
      {/* KPI Cards */}

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-2">
        {statCards.map((stat) => (
          <StatCard key={stat.label} {...stat} />
        ))}
      </div>

      {/* Tables */}

      <div className="grid lg:grid-cols-2 gap-3">
        {/* Recent Orders */}

        <ChartCard title="Recent Orders" description="Recently placed orders.">
          <DataTable
            columns={[
              {
                key: "order_id",
                label: "Order ID",
              },
              {
                key: "customer_state",
                label: "State",
              },
              {
                key: "category",
                label: "Category",
              },
              {
                key: "amount",
                label: "Amount",
                render: (value) => formatCurrency(value),
              },
              {
                key: "status",
                label: "Status",
              },
              {
                key: "date",
                label: "Date",
              },
            ]}
            rows={recent_orders}
          />
        </ChartCard>

        {/* Top Categories */}

        <ChartCard
          title="Top Categories"
          description="Top categories by revenue."
        >
          <DataTable
            columns={[
              {
                key: "category",
                label: "Category",
              },
              {
                key: "orders",
                label: "Orders",
              },
              {
                key: "revenue",
                label: "Revenue",
                render: (value) => formatCurrency(value),
              },
            ]}
            rows={top_categories}
          />
        </ChartCard>
      </div>
    </div>
  );
}

export default CurrentDashboard;
