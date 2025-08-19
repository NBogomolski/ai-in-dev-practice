const DAYS_IN_MONTH = 30;

/** @type {{ category: string; amount: number; }[]} */
let expenses = [];

const sampleExpenses = [
  { category: "Groceries", amount: 15000 },
  { category: "Rent", amount: 40000 },
  { category: "Transportation", amount: 5000 },
  { category: "Entertainment", amount: 10000 },
  { category: "Communication", amount: 2000 },
  { category: "Gym", amount: 3000 },
];

// DOM Elements
const tbody = document.getElementById("expenses-tbody");
const inputCategory = document.getElementById("input-category");
const inputAmount = document.getElementById("input-amount");
const btnAdd = document.getElementById("btn-add");
const btnCalc = document.getElementById("btn-calc");
const btnClear = document.getElementById("btn-clear");
const btnSample = document.getElementById("btn-sample");

const resultTotal = document.getElementById("result-total");
const resultAverage = document.getElementById("result-average");
const resultTop3 = document.getElementById("result-top3");

function formatCurrency(value) {
  if (Number.isNaN(value) || value == null) return "$0";
  // Show up to 2 decimals if needed
  const hasFraction = Math.abs(value % 1) > 0;
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: hasFraction ? 2 : 0,
    maximumFractionDigits: hasFraction ? 2 : 0,
  }).format(value);
}

function parseAmount(raw) {
  if (typeof raw !== "string") return NaN;
  const normalized = raw.replace(/[$,\s]/g, "");
  if (normalized === "") return NaN;
  const num = Number(normalized);
  return Number.isFinite(num) ? num : NaN;
}

function clearInputs() {
  inputCategory.value = "";
  inputAmount.value = "";
  inputCategory.focus();
}

function handleAddExpense() {
  const category = inputCategory.value.trim();
  const amount = parseAmount(inputAmount.value);

  if (!category) {
    alert("Please enter a category.");
    inputCategory.focus();
    return;
  }
  if (!Number.isFinite(amount) || amount < 0) {
    alert("Please enter a valid non-negative amount.");
    inputAmount.focus();
    return;
  }

  expenses.push({ category, amount });
  renderTable();
  clearInputs();
}

function handleDeleteExpense(index) {
  expenses.splice(index, 1);
  renderTable();
}

function renderTable() {
  tbody.innerHTML = "";
  expenses.forEach((item, index) => {
    const tr = document.createElement("tr");

    const tdCategory = document.createElement("td");
    tdCategory.textContent = item.category;

    const tdAmount = document.createElement("td");
    tdAmount.className = "amount";
    tdAmount.textContent = formatCurrency(item.amount);

    const tdActions = document.createElement("td");
    tdActions.className = "actions";
    const delBtn = document.createElement("button");
    delBtn.className = "delete-btn";
    delBtn.type = "button";
    delBtn.title = "Delete";
    delBtn.textContent = "Delete";
    delBtn.addEventListener("click", () => handleDeleteExpense(index));
    tdActions.appendChild(delBtn);

    tr.appendChild(tdCategory);
    tr.appendChild(tdAmount);
    tr.appendChild(tdActions);
    tbody.appendChild(tr);
  });
}

function calculateIndicators() {
  const total = expenses.reduce((sum, e) => sum + e.amount, 0);
  const averagePerDay = total / DAYS_IN_MONTH;
  const top3 = [...expenses]
    .sort((a, b) => b.amount - a.amount)
    .slice(0, 3);

  resultTotal.textContent = formatCurrency(total);
  resultAverage.textContent = formatCurrency(Math.round(averagePerDay * 100) / 100);

  resultTop3.innerHTML = "";
  top3.forEach(item => {
    const li = document.createElement("li");
    li.textContent = `${item.category} (${formatCurrency(item.amount)})`;
    resultTop3.appendChild(li);
  });
}

function clearAll() {
  expenses = [];
  renderTable();
  calculateIndicators();
}

function loadSample() {
  expenses = sampleExpenses.map(e => ({ ...e }));
  renderTable();
  calculateIndicators();
}

function wireEvents() {
  btnAdd.addEventListener("click", handleAddExpense);
  btnCalc.addEventListener("click", calculateIndicators);
  btnClear.addEventListener("click", clearAll);
  btnSample.addEventListener("click", loadSample);

  inputAmount.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      handleAddExpense();
    }
  });
  inputCategory.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      handleAddExpense();
    }
  });
}

// Initialize
wireEvents();
loadSample();


