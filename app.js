const stationTableBody = document.getElementById('stationsTableBody');
const requestsTableBody = document.getElementById('requestsTableBody');
const greedySummary = document.getElementById('greedySummary');
const dpSummary = document.getElementById('dpSummary');
const greedyList = document.getElementById('greedyList');
const dpList = document.getElementById('dpList');

const sampleStations = [
  { station_id: 'CS-01', power_kwh_per_slot: 20, cost_per_slot: 6.0 },
  { station_id: 'CS-02', power_kwh_per_slot: 30, cost_per_slot: 8.0 },
  { station_id: 'CS-03', power_kwh_per_slot: 15, cost_per_slot: 4.0 }
];

const sampleRequests = [
  { vehicle_id: 'EV-101', arrival_slot: 0, departure_slot: 4, energy_needed_kwh: 40, priority: 3 },
  { vehicle_id: 'EV-102', arrival_slot: 0, departure_slot: 3, energy_needed_kwh: 30, priority: 2 },
  { vehicle_id: 'EV-103', arrival_slot: 1, departure_slot: 5, energy_needed_kwh: 50, priority: 4 },
  { vehicle_id: 'EV-104', arrival_slot: 2, departure_slot: 6, energy_needed_kwh: 35, priority: 1 },
  { vehicle_id: 'EV-105', arrival_slot: 3, departure_slot: 7, energy_needed_kwh: 60, priority: 5 },
  { vehicle_id: 'EV-106', arrival_slot: 4, departure_slot: 8, energy_needed_kwh: 25, priority: 2 }
];

let stations = structuredClone(sampleStations);
let requests = structuredClone(sampleRequests);

function createStationRow(station, index) {
  const tr = document.createElement('tr');
  tr.innerHTML = `
    <td><input type="text" value="${station.station_id}" data-field="station_id" data-index="${index}" /></td>
    <td><input type="number" min="1" step="1" value="${station.power_kwh_per_slot}" data-field="power_kwh_per_slot" data-index="${index}" /></td>
    <td><input type="number" min="0" step="0.1" value="${station.cost_per_slot}" data-field="cost_per_slot" data-index="${index}" /></td>
    <td><button class="delete-btn" aria-label="Remove station" data-remove-station="${index}">×</button></td>
  `;
  return tr;
}

function createRequestRow(request, index) {
  const tr = document.createElement('tr');
  tr.innerHTML = `
    <td><input type="text" value="${request.vehicle_id}" data-field="vehicle_id" data-index="${index}" /></td>
    <td><input type="number" step="1" value="${request.arrival_slot}" data-field="arrival_slot" data-index="${index}" /></td>
    <td><input type="number" step="1" value="${request.departure_slot}" data-field="departure_slot" data-index="${index}" /></td>
    <td><input type="number" min="0.1" step="0.5" value="${request.energy_needed_kwh}" data-field="energy_needed_kwh" data-index="${index}" /></td>
    <td><input type="number" min="1" step="1" value="${request.priority}" data-field="priority" data-index="${index}" /></td>
    <td><button class="delete-btn" aria-label="Remove request" data-remove-request="${index}">×</button></td>
  `;
  return tr;
}

function renderStations() {
  stationTableBody.innerHTML = '';
  stations.forEach((station, index) => {
    stationTableBody.appendChild(createStationRow(station, index));
  });
}

function renderRequests() {
  requestsTableBody.innerHTML = '';
  requests.forEach((request, index) => {
    requestsTableBody.appendChild(createRequestRow(request, index));
  });
}

function syncDataFromForm() {
  stations = Array.from(document.querySelectorAll('#stationsTableBody tr')).map((row) => ({
    station_id: row.querySelector('[data-field="station_id"]').value || 'STN',
    power_kwh_per_slot: Number(row.querySelector('[data-field="power_kwh_per_slot"]').value || 0),
    cost_per_slot: Number(row.querySelector('[data-field="cost_per_slot"]').value || 0)
  }));

  requests = Array.from(document.querySelectorAll('#requestsTableBody tr')).map((row) => ({
    vehicle_id: row.querySelector('[data-field="vehicle_id"]').value || 'EV-NEW',
    arrival_slot: Number(row.querySelector('[data-field="arrival_slot"]').value || 0),
    departure_slot: Number(row.querySelector('[data-field="departure_slot"]').value || 1),
    energy_needed_kwh: Number(row.querySelector('[data-field="energy_needed_kwh"]').value || 0),
    priority: Number(row.querySelector('[data-field="priority"]').value || 1)
  }));
}

function updateSummary(container, result) {
  container.innerHTML = `
    <span class="summary-badge">Total energy: ${result.total_energy_kwh.toFixed(1)} kWh</span>
    <span class="summary-badge">Total cost: $${result.total_cost.toFixed(2)}</span>
    <span class="summary-badge">Rejected: ${result.rejected_vehicle_ids.length ? result.rejected_vehicle_ids.join(', ') : 'None'}</span>
  `;
}

function updateList(container, result) {
  if (!result.schedules.length) {
    container.innerHTML = '<div class="empty-state">No valid scheduling assignments found.</div>';
    return;
  }

  container.innerHTML = result.schedules
    .map((item) => `
      <div class="schedule-row">
        <div><strong>${item.vehicle_id}</strong></div>
        <div>${item.station_id}</div>
        <div>slot ${item.start_slot}-${item.end_slot}</div>
        <div>${item.energy_delivered_kwh.toFixed(1)} kWh</div>
        <div>$${item.cost.toFixed(2)}</div>
      </div>
    `)
    .join('');
}

function scheduleGreedy(stationsList, requestsList) {
  const schedules = [];
  const rejected = [];
  const stationUsage = Object.fromEntries(stationsList.map((station) => [station.station_id, []]));

  const sorted = [...requestsList].sort((a, b) => {
    return a.departure_slot - b.departure_slot || a.priority - b.priority || a.energy_needed_kwh - b.energy_needed_kwh || a.arrival_slot - b.arrival_slot;
  });

  for (const request of sorted) {
    let assigned = false;

    for (const station of stationsList) {
      const duration = Math.max(1, request.departure_slot - request.arrival_slot);
      const energyCapacity = station.power_kwh_per_slot * duration;

      if (request.energy_needed_kwh > energyCapacity) {
        continue;
      }

      const conflict = stationUsage[station.station_id].some(([start, end]) => {
        return !(request.departure_slot <= start || request.arrival_slot >= end);
      });

      if (conflict) {
        continue;
      }

      const startSlot = request.arrival_slot;
      const endSlot = request.departure_slot;
      const session = {
        vehicle_id: request.vehicle_id,
        station_id: station.station_id,
        start_slot: startSlot,
        end_slot: endSlot,
        energy_delivered_kwh: Math.min(request.energy_needed_kwh, energyCapacity),
        cost: (endSlot - startSlot) * station.cost_per_slot
      };

      schedules.push(session);
      stationUsage[station.station_id].push([startSlot, endSlot]);
      assigned = true;
      break;
    }

    if (!assigned) {
      rejected.push(request.vehicle_id);
    }
  }

  return {
    schedules,
    total_energy_kwh: schedules.reduce((sum, session) => sum + session.energy_delivered_kwh, 0),
    total_cost: schedules.reduce((sum, session) => sum + session.cost, 0),
    rejected_vehicle_ids: rejected
  };
}

function scheduleDynamicProgramming(stationsList, requestsList) {
  const feasibleSessions = [];

  for (const request of requestsList) {
    for (const station of stationsList) {
      const duration = Math.max(1, request.departure_slot - request.arrival_slot);
      const availableEnergy = station.power_kwh_per_slot * duration;

      if (request.energy_needed_kwh <= availableEnergy) {
        feasibleSessions.push({
          vehicle_id: request.vehicle_id,
          station_id: station.station_id,
          start_slot: request.arrival_slot,
          end_slot: request.departure_slot,
          energy_delivered_kwh: request.energy_needed_kwh,
          cost: duration * station.cost_per_slot,
          value: request.priority * request.energy_needed_kwh
        });
      }
    }
  }

  if (!feasibleSessions.length) {
    return {
      schedules: [],
      total_energy_kwh: 0,
      total_cost: 0,
      rejected_vehicle_ids: requestsList.map((request) => request.vehicle_id)
    };
  }

  feasibleSessions.sort((a, b) => a.end_slot - b.end_slot || a.start_slot - b.start_slot);

  const n = feasibleSessions.length;
  const dp = Array.from({ length: n + 1 }, () => ({ value: 0, chosen: [] }));

  for (let i = 1; i <= n; i++) {
    let j = i - 1;
    while (j >= 0 && feasibleSessions[j].end_slot > feasibleSessions[i - 1].start_slot) {
      j--;
    }

    const withCurrent = feasibleSessions[i - 1].value + dp[j + 1].value;
    const withoutCurrent = dp[i - 1].value;

    if (withCurrent > withoutCurrent) {
      dp[i] = {
        value: withCurrent,
        chosen: [...dp[j + 1].chosen, feasibleSessions[i - 1]]
      };
    } else {
      dp[i] = { value: withoutCurrent, chosen: [...dp[i - 1].chosen] };
    }
  }

  const selected = dp[n].chosen;
  const rejected = requestsList
    .filter((request) => !selected.some((item) => item.vehicle_id === request.vehicle_id))
    .map((request) => request.vehicle_id);

  return {
    schedules: selected,
    total_energy_kwh: selected.reduce((sum, session) => sum + session.energy_delivered_kwh, 0),
    total_cost: selected.reduce((sum, session) => sum + session.cost, 0),
    rejected_vehicle_ids: rejected
  };
}

function renderResults() {
  syncDataFromForm();
  const greedyResult = scheduleGreedy(stations, requests);
  const dpResult = scheduleDynamicProgramming(stations, requests);

  updateSummary(greedySummary, greedyResult);
  updateList(greedyList, greedyResult);

  updateSummary(dpSummary, dpResult);
  updateList(dpList, dpResult);
}

function addStation() {
  stations.push({ station_id: `CS-${stations.length + 1}`.padStart(4, '0'), power_kwh_per_slot: 10, cost_per_slot: 5 });
  renderStations();
}

function addRequest() {
  requests.push({ vehicle_id: `EV-${requests.length + 1}`, arrival_slot: 0, departure_slot: 4, energy_needed_kwh: 20, priority: 1 });
  renderRequests();
}

function removeStation(index) {
  stations.splice(index, 1);
  renderStations();
  renderResults();
}

function removeRequest(index) {
  requests.splice(index, 1);
  renderRequests();
  renderResults();
}

document.getElementById('loadSampleBtn').addEventListener('click', () => {
  stations = structuredClone(sampleStations);
  requests = structuredClone(sampleRequests);
  renderStations();
  renderRequests();
  renderResults();
});

document.getElementById('addStationBtn').addEventListener('click', addStation);
document.getElementById('addRequestBtn').addEventListener('click', addRequest);
document.getElementById('greedyBtn').addEventListener('click', renderResults);
document.getElementById('dpBtn').addEventListener('click', renderResults);

stationTableBody.addEventListener('input', renderResults);
requestsTableBody.addEventListener('input', renderResults);
stationTableBody.addEventListener('click', (event) => {
  const removeBtn = event.target.closest('[data-remove-station]');
  if (removeBtn) {
    removeStation(Number(removeBtn.dataset.removeStation));
  }
});
requestsTableBody.addEventListener('click', (event) => {
  const removeBtn = event.target.closest('[data-remove-request]');
  if (removeBtn) {
    removeRequest(Number(removeBtn.dataset.removeRequest));
  }
});

renderStations();
renderRequests();
renderResults();
