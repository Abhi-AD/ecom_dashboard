const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const apptable = document.querySelector(".app-table");
const tablebody = document.querySelector(".table-body");
const paginationContainer = document.querySelector(".pagination-container");

tableOutput.style.display = "none";
searchField.addEventListener("keyup", (e) => {
  const searchValue = e.target.value;
  if (searchValue.trim().length > 0) {
    paginationContainer.style.display = "none";
    tablebody.innerHTML = "";
    console.log("searchField", searchValue);
    fetch("/income/search-income/", {
      body: JSON.stringify({ searchText: searchValue }),
      method: "POST",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Date", data);
        tableOutput.style.display = "block";
        apptable.style.display = "none";
        if (data.length === 0) {
          tableOutput.innerHTML = "No results found";
        } else {
          data.forEach((income) => {
            // Format the date
            const formattedDate = new Date(income.date).toLocaleDateString(
              "en-US",
              {
                year: "numeric",
                month: "short",
                day: "numeric",
              }
            );
            tablebody.innerHTML += `
              <tr>
                <td>${income.amount}</td>
                <td>${income.source}</td>
                <td>${income.description}</td>
                <td>${formattedDate}</td>
                <td>
                  <a href="/income-edit/${income.id}/" class="btn btn-secondary btn-sm">Edit</a>
                  <a href="/income-delete/${income.id}/" class="btn btn-danger btn-sm">Delete</a>
                </td>
              </tr>
            `;
          });
        }
      });
  } else {
    tableOutput.style.display = "none";
    apptable.style.display = "block";
    paginationContainer.style.display = "block";
  }
});
