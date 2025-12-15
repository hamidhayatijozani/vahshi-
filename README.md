# vahshi-
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>KhoarForex Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
  <h2>KhoarForexSystem Live Dashboard</h2>
  <canvas id="priceChart" width="800" height="400"></canvas>
  <div id="signalBox"></div>

  <script>
    const ctx = document.getElementById('priceChart').getContext('2d');
    const chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: [],
        datasets: [{
          label: 'EURUSD Price',
          data: [],
          borderColor: 'blue',
          fill: false
        }]
      }
    });

    const signalBox = document.getElementById('signalBox');

    // اتصال به WebSocket سرور
    const ws = new WebSocket("ws://localhost:8765");

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const time = new Date(data.timestamp).toLocaleTimeString();

      // اضافه کردن داده جدید به نمودار
      chart.data.labels.push(time);
      chart.data.datasets[0].data.push(data.price);
      chart.update();

      // نمایش سیگنال نهایی
      signalBox.innerHTML = `
        <p><strong>Action:</strong> ${data.final_decision.action}</p>
        <p><strong>Confidence:</strong> ${data.final_decision.confidence}</p>
        <p><strong>Warnings:</strong> ${data.warnings}</p>
      `;
    };
  </script>
</body>
</html>