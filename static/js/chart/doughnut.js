// Ensure you have installed chartjs-plugin-datalabels
// npm install chartjs-plugin-datalabels

const generateColors = (numColors) => {
  const colors = [];
  for (let i = 0; i < numColors; i++) {
    const randomColor = `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(
      Math.random() * 255
    )}, ${Math.floor(Math.random() * 255)}, 0.7)`;
    colors.push(randomColor);
  }
  return colors;
};

const renderChart = (data, labels) => {
  const ctx = document.getElementById("data").getContext("2d");
  const backgroundColors = generateColors(labels.length);

  // Calculate total and percentage for each data value
  const total = data.reduce((acc, value) => acc + value, 0);
  const percentages = data.map((value) => ((value / total) * 100).toFixed(2));

  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Last 6 months expense",
          data: data,
          backgroundColor: backgroundColors,
          borderColor: backgroundColors,
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: "Expenses by category: " + total,
          font: {
            size: 30,
          },
        },
        legend: {
          labels: {
            font: {
              size: 20,
            },
          },
        },
        tooltip: {
          callbacks: {
            label: function (tooltipItem) {
              const percentage = percentages[tooltipItem.dataIndex];
              const value = tooltipItem.raw;
              return `${tooltipItem.label}: ${value} (${percentage}%)`;
            },
          },
        },
        datalabels: {
          display: true,
          color: "white",
          font: {
            weight: "bold",
            size: 16,
          },
          formatter: function (value, context) {
            const percentage = percentages[context.dataIndex];
            const totalValue = value;
            return `${totalValue} (${percentage}%)`;
          },
        },
      },
    },
  });
};

const getChartData = () => {
  fetch("/expense-category-summary/")
    .then((response) => response.json())
    .then((result) => {
      const category_data = result.expense_category_date;
      const [labels, data] = [
        Object.keys(category_data),
        Object.values(category_data),
      ];
      renderChart(data, labels);
    })
    .catch((error) => console.error("Error:", error));
};

document.onload = getChartData();
a;
