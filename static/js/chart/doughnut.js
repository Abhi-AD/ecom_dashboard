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
  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Last 6 months expense",
          data: data,
          backgroundColor: backgroundColors,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: "Expenses by category",
        },
        legend: {
          labels: {
            font: {
              size: 20,
            },
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
