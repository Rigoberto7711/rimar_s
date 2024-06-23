document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault();
    let searchValue = document.getElementById('searchInput').value;
    
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'term=' + encodeURIComponent(searchValue)
    })
    .then(response => response.json())
    .then(data => {
        let resultsContainer = document.getElementById('searchResults');
        resultsContainer.innerHTML = ''; // Limpiar resultados anteriores
        data.forEach(account => {
            let accountElement = document.createElement('div');
            accountElement.textContent = account.nombre_cuenta;
            accountElement.onclick = function() {
                addAccountToList(account);
            };
            resultsContainer.appendChild(accountElement);
        });
    });
});

function addAccountToList(account) {
    let selectedAccountsList = document.getElementById('selectedAccounts');
    let accountItem = document.createElement('li');
    accountItem.textContent = account.nombre_cuenta;
    selectedAccountsList.appendChild(accountItem);
}
