const ICONS = {
  heart: '<path d="M12 21s-7.5-4.6-10-9.3C.5 8.4 2.4 5 5.8 5c2 0 3.4 1.1 4.2 2.4C10.8 6.1 12.2 5 14.2 5c3.4 0 5.3 3.4 3.8 6.7C19.5 16.4 12 21 12 21z" stroke="currentColor" stroke-width="2" fill="none"/>',
  droplet: '<path d="M12 2s6 7.2 6 11.5A6 6 0 016 13.5C6 9.2 12 2 12 2z" stroke="currentColor" stroke-width="2" fill="none" stroke-linejoin="round"/>',
  activity: '<path d="M3 12h4l2 8 4-16 2 8h6" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
  shield: '<path d="M12 3l7 3v6c0 5-3 8-7 9-4-1-7-4-7-9V6l7-3z" stroke="currentColor" stroke-width="2" fill="none" stroke-linejoin="round"/>',
  flame: '<path d="M12 2s-2 3-2 5.5c0 1 1 2 2 2s2-1 2-2C14 5 12 2 12 2zM6 13a6 6 0 0012 0c0-3-2-5-3-7 0 2-1 3-2 3s-2-1-2-3c-2 2-5 4-5 7z" stroke="currentColor" stroke-width="1.6" fill="none" stroke-linejoin="round"/>',
};

const state = {
  category: "kidney",
  mode: "search",
  stageIndex: 0,
  variantIndex: 0,
  generated: false,
  lastGeneratedDateKey: null,
};

const SAVE_KEY = "dietGuideSavedPlans";
const USER_FOODS_KEY = "dietGuideUserFoods";
let currentPlanSnapshot = null;

function loadUserFoods() {
  try {
    return JSON.parse(localStorage.getItem(USER_FOODS_KEY) || "{}");
  } catch (e) {
    return {};
  }
}

function saveUserFoods(all) {
  localStorage.setItem(USER_FOODS_KEY, JSON.stringify(all));
}

function getUserFoods(catKey) {
  return loadUserFoods()[catKey] || [];
}

// perCategory: { [categoryKey]: { status, desc } } — one verdict per condition,
// all sharing the same id so a single delete removes it everywhere.
function addUserFood(name, perCategory) {
  const all = loadUserFoods();
  const id = `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
  for (const catKey of Object.keys(CATEGORIES)) {
    if (!all[catKey]) all[catKey] = [];
    const entry = perCategory[catKey];
    all[catKey].push({ id, name, status: entry.status, desc: entry.desc });
  }
  saveUserFoods(all);
}

function deleteUserFood(id) {
  const all = loadUserFoods();
  for (const catKey of Object.keys(all)) {
    all[catKey] = all[catKey].filter((f) => f.id !== id);
  }
  saveUserFoods(all);
}

function todayKey() {
  const d = new Date();
  return `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}`;
}

// Deterministic per-day index so the "today's plan" is the same all day but
// changes automatically once the date rolls over, without requiring a click.
function dailyVariantIndex(stageKey, count) {
  const key = `${todayKey()}|${stageKey}`;
  let hash = 0;
  for (let i = 0; i < key.length; i++) {
    hash = (hash * 31 + key.charCodeAt(i)) >>> 0;
  }
  return hash % count;
}

function iconSvg(name, extraClass = "") {
  return `<svg class="icon ${extraClass}" viewBox="0 0 24 24" fill="none">${ICONS[name] || ""}</svg>`;
}

function renderCategoryTabs() {
  const nav = document.getElementById("categoryTabs");
  nav.innerHTML = Object.entries(CATEGORIES)
    .map(
      ([key, cat]) => `
      <button class="category-tab ${key === state.category ? "active" : ""}" data-category="${key}">
        ${iconSvg(cat.icon)}
        ${cat.label}
      </button>`
    )
    .join("");

  nav.querySelectorAll(".category-tab").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.category = btn.dataset.category;
      state.stageIndex = 0;
      state.variantIndex = 0;
      state.generated = false;
      renderCategoryTabs();
      renderSearchPanel();
      renderPlanPanel();
    });
  });
}

function renderSegmented() {
  document.querySelectorAll(".segment-btn").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.mode === state.mode);
  });
  document.getElementById("searchPanel").classList.toggle("hidden", state.mode !== "search");
  document.getElementById("planPanel").classList.toggle("hidden", state.mode !== "plan");
}

function statusBadge(status) {
  const meta = STATUS_META[status];
  return `<span class="status-badge ${meta.className}">${meta.label}</span>`;
}

function renderResults(matches, recipeMatches, query) {
  const results = document.getElementById("results");
  if (!query) {
    results.innerHTML = "";
    return;
  }

  const verdictHtml = matches
    .map(
      (food) => `
      <div class="result-card ${STATUS_META[food.status].className}">
        <div style="flex:1">
          <p class="result-name">${escapeHtml(food.name)} ${food.custom ? '<span class="custom-badge">직접 추가</span>' : ""}</p>
          <p class="result-desc">${escapeHtml(food.desc)}</p>
        </div>
        <div class="result-actions">
          ${statusBadge(food.status)}
          ${food.custom ? `<button type="button" class="delete-food-btn" data-delete-food="${food.id}">삭제</button>` : ""}
        </div>
      </div>`
    )
    .join("");

  const recipeHtml =
    recipeMatches.length === 0
      ? ""
      : `
      <div class="recipe-search-section">
        <p class="recipe-search-label">🍳 관련 요리 레시피</p>
        <div class="recipe-search-grid">
          ${recipeMatches
            .map(
              (r) => `
            <button type="button" class="food-item recipe-search-item" data-food="${escapeHtml(r.name)}">
              <span class="food-name">${escapeHtml(r.name)}</span>
              <p class="food-desc">${escapeHtml(r.recipe.desc)}</p>
            </button>`
            )
            .join("")}
        </div>
      </div>`;

  const addFoodHtml =
    matches.length > 0
      ? ""
      : `
      <div class="add-food-box">
        <p class="add-food-label">"${escapeHtml(query)}"에 대한 등록된 음식 정보가 없습니다.</p>
        <p class="add-food-fetch-status" id="addFoodFetchStatus">🔍 인터넷에서 정보를 찾는 중...</p>
        <textarea id="addFoodDesc" placeholder="기본 설명 (참고용 — 아래에서 카테고리별 이유를 따로 적지 않으면 이 설명이 그대로 쓰입니다)"></textarea>
        <p class="status-choice-label">아래 5개 조건 각각에 대해 장단점을 확인하고 등급을 선택하세요</p>
        <div class="category-verdict-rows">
          ${Object.entries(CATEGORIES)
            .map(
              ([key, cat]) => `
            <div class="category-verdict-row" data-cat-row="${key}">
              <p class="category-verdict-label">${iconSvg(cat.icon)} ${cat.label}</p>
              <div class="status-choice-row">
                <label><input type="radio" name="status-${key}" value="good" /> 적합</label>
                <label><input type="radio" name="status-${key}" value="caution" /> 주의</label>
                <label><input type="radio" name="status-${key}" value="bad" /> 부적합</label>
              </div>
              <input type="text" class="category-reason-input" data-cat-reason="${key}" placeholder="${cat.label}에서의 이유 (선택 — 비우면 기본 설명 사용)" />
            </div>`
            )
            .join("")}
        </div>
        <button type="button" class="add-food-btn" data-add-food="${escapeHtml(query)}">"${escapeHtml(query)}" 모든 카테고리에 추가하기</button>
      </div>`;

  if (matches.length === 0 && recipeMatches.length === 0) {
    results.innerHTML = addFoodHtml;
    return;
  }

  results.innerHTML = verdictHtml + recipeHtml + addFoodHtml;
}

function searchRecipeDb(query, excludeNames) {
  const q = query.toLowerCase();
  const names = [...Object.keys(RECIPE_DB), ...Object.keys(RECIPE_ALIASES)];
  const seen = new Set();
  const results = [];
  for (const name of names) {
    if (seen.has(name) || excludeNames.has(name)) continue;
    if (name.toLowerCase().includes(q) || q.includes(name.toLowerCase())) {
      seen.add(name);
      results.push({ name, recipe: getRecipe(name) });
    }
  }
  return results;
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

function doSearch() {
  const cat = CATEGORIES[state.category];
  const query = document.getElementById("searchInput").value.trim();
  if (!query) {
    renderResults([], [], "");
    return;
  }
  const q = query.toLowerCase();
  const curatedMatches = cat.foods.filter((f) => f.name.toLowerCase().includes(q) || q.includes(f.name.toLowerCase()));
  const userMatches = getUserFoods(state.category)
    .filter((f) => f.name.toLowerCase().includes(q) || q.includes(f.name.toLowerCase()))
    .map((f) => ({ ...f, custom: true }));
  const matches = [...curatedMatches, ...userMatches];
  const excludeNames = new Set(matches.map((f) => f.name));
  const recipeMatches = searchRecipeDb(query, excludeNames);
  renderResults(matches, recipeMatches, query);

  if (matches.length === 0) {
    autoFillFoodDescription(query);
  }
}

// Looks up a plain-language summary from Korean Wikipedia's public REST API
// (no key needed, CORS-enabled) to help pre-fill the description. The user
// still has to read it and pick 적합/주의/부적합 themselves — this never
// guesses the health verdict on its own.
async function fetchWikiSummary(name) {
  try {
    const res = await fetch(`https://ko.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(name)}`);
    if (!res.ok) return null;
    const data = await res.json();
    if (!data.extract || data.type === "disambiguation") return null;
    return data.extract;
  } catch (e) {
    return null;
  }
}

async function autoFillFoodDescription(query) {
  const extract = await fetchWikiSummary(query);

  // The user may have searched something else while this was in flight.
  if (document.getElementById("searchInput").value.trim() !== query) return;
  const statusEl = document.getElementById("addFoodFetchStatus");
  const textarea = document.getElementById("addFoodDesc");
  if (!statusEl || !textarea) return;

  if (extract) {
    textarea.value = extract.length > 160 ? extract.slice(0, 160).trim() + "…" : extract;
    statusEl.textContent = "🔍 인터넷에서 가져온 설명입니다. 내용을 확인하고 필요하면 수정한 뒤, 아래 5개 조건별로 등급을 선택하세요.";
  } else {
    statusEl.textContent = "인터넷에서 관련 정보를 찾지 못했습니다. 아래에 직접 설명을 입력해주세요.";
  }
}

function renderChips() {
  const cat = CATEGORIES[state.category];
  const sample = cat.foods.slice(0, 6);
  const chipRow = document.getElementById("chipRow");
  chipRow.innerHTML = sample
    .map((f) => `<button class="chip" data-name="${escapeHtml(f.name)}">${escapeHtml(f.name)}</button>`)
    .join("");
  chipRow.querySelectorAll(".chip").forEach((chip) => {
    chip.addEventListener("click", () => {
      document.getElementById("searchInput").value = chip.dataset.name;
      doSearch();
    });
  });
}

function renderSearchPanel() {
  const cat = CATEGORIES[state.category];
  document.getElementById("searchIntro").textContent = cat.intro;
  document.getElementById("searchNote").textContent = cat.note;
  document.getElementById("searchInput").value = "";
  renderChips();
  renderResults([], [], "");
}

function renderStageSelect() {
  const cat = CATEGORIES[state.category];
  const select = document.getElementById("stageSelect");
  select.innerHTML = cat.stages
    .map((stage, i) => `<option value="${i}">${escapeHtml(stage.label)}</option>`)
    .join("");
  select.value = String(state.stageIndex);
}

function renderPlanPanel() {
  renderStageSelect();
  document.getElementById("planResult").classList.add("hidden");
}

function renderMealSections(meals) {
  const sections = [
    ["아침", meals.breakfast],
    ["점심", meals.lunch],
    ["저녁", meals.dinner],
    ["간식", meals.snack],
  ];

  document.getElementById("mealGrid").innerHTML = sections
    .map(([label, items]) => {
      const kcalSum = items.reduce((sum, item) => sum + (getRecipe(item).kcal || 0), 0);
      const itemsHtml = items
        .map((item) => {
          const recipe = getRecipe(item);
          return `
          <li>
            <button type="button" class="food-item" data-food="${escapeHtml(item)}">
              <span class="food-name">${escapeHtml(item)}</span>
              <p class="food-desc">${escapeHtml(recipe.desc)}</p>
            </button>
          </li>`;
        })
        .join("");
      return `
      <div class="meal-card">
        <h3>${label}</h3>
        <p class="meal-kcal">약 ${kcalSum}kcal</p>
        <ul>${itemsHtml}</ul>
      </div>`;
    })
    .join("");
}

function resetSaveButton() {
  const btn = document.getElementById("saveBtn");
  btn.classList.remove("saved");
  document.getElementById("saveBtnLabel").textContent = "이 식단 저장하기";
}

function showPlanResult(snapshot) {
  currentPlanSnapshot = snapshot;
  document.getElementById("planTitle").textContent = `${snapshot.categoryLabel} · ${snapshot.title}`;
  document.getElementById("planNote").textContent = snapshot.guidance;
  renderMealSections(snapshot.meals);
  document.getElementById("planResult").classList.remove("hidden");
  resetSaveButton();
}

function renderPlanResult() {
  const cat = CATEGORIES[state.category];
  const stage = cat.stages[state.stageIndex];
  const plan = stage.meals[state.variantIndex % stage.meals.length];

  showPlanResult({
    categoryLabel: cat.label,
    title: `${stage.label} - ${plan.title}`,
    guidance: stage.guidance,
    meals: {
      breakfast: plan.breakfast,
      lunch: plan.lunch,
      dinner: plan.dinner,
      snack: plan.snack,
    },
  });
}

function openRecipeModal(name) {
  const recipe = getRecipe(name);
  document.getElementById("modalFoodName").textContent = name;
  document.getElementById("modalKcal").textContent = recipe.kcal != null ? `약 ${recipe.kcal}kcal` : "";
  document.getElementById("modalDesc").textContent = recipe.desc;

  const bodyEl = document.getElementById("modalRecipeBody");
  const hasRecipe = recipe.ingredients.length > 0 || recipe.steps.length > 0;
  bodyEl.classList.toggle("hidden", !hasRecipe);
  if (hasRecipe) {
    document.getElementById("modalIngredients").innerHTML = recipe.ingredients
      .map((i) => `<li>${escapeHtml(i)}</li>`)
      .join("");
    document.getElementById("modalSteps").innerHTML = recipe.steps.map((s) => `<li>${escapeHtml(s)}</li>`).join("");
  }

  document.getElementById("recipeModal").classList.remove("hidden");
}

function closeRecipeModal() {
  document.getElementById("recipeModal").classList.add("hidden");
}

function loadSavedPlans() {
  try {
    return JSON.parse(localStorage.getItem(SAVE_KEY) || "[]");
  } catch (e) {
    return [];
  }
}

function writeSavedPlans(list) {
  localStorage.setItem(SAVE_KEY, JSON.stringify(list));
}

function renderSavedList() {
  const list = loadSavedPlans();
  const countEl = document.getElementById("savedCount");
  countEl.textContent = list.length ? `(${list.length})` : "";

  const container = document.getElementById("savedList");
  if (list.length === 0) {
    container.innerHTML = `<p class="saved-empty">아직 저장된 식단이 없습니다. 마음에 드는 식단을 저장해보세요.</p>`;
    return;
  }

  container.innerHTML = list
    .slice()
    .reverse()
    .map(
      (p) => `
      <div class="saved-item">
        <div class="saved-item-info">
          <p class="saved-item-title">${escapeHtml(p.title)}</p>
          <p class="saved-item-meta">${escapeHtml(p.categoryLabel)} · ${escapeHtml(p.savedAtLabel)}</p>
        </div>
        <div class="saved-item-actions">
          <button type="button" class="saved-view-btn" data-view="${p.id}">보기</button>
          <button type="button" class="saved-delete-btn" data-delete="${p.id}">삭제</button>
        </div>
      </div>`
    )
    .join("");
}

function init() {
  renderCategoryTabs();
  renderSegmented();
  renderSearchPanel();
  renderPlanPanel();

  document.querySelectorAll(".segment-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.mode = btn.dataset.mode;
      renderSegmented();
    });
  });

  document.getElementById("searchBtn").addEventListener("click", doSearch);
  document.getElementById("searchInput").addEventListener("keydown", (e) => {
    if (e.key === "Enter") doSearch();
  });

  document.getElementById("results").addEventListener("click", (e) => {
    const addBtn = e.target.closest("[data-add-food]");
    if (addBtn) {
      const name = addBtn.dataset.addFood;
      const baseDesc = document.getElementById("addFoodDesc").value.trim();
      if (!baseDesc) {
        document.getElementById("addFoodDesc").focus();
        return;
      }

      const perCategory = {};
      for (const catKey of Object.keys(CATEGORIES)) {
        const statusInput = document.querySelector(`input[name="status-${catKey}"]:checked`);
        if (!statusInput) {
          document.getElementById("addFoodFetchStatus").textContent = `"${CATEGORIES[catKey].label}" 조건의 등급을 아직 선택하지 않았습니다. 5개 조건 모두 확인 후 선택해주세요.`;
          document.querySelector(`[data-cat-row="${catKey}"]`).scrollIntoView({ behavior: "smooth", block: "center" });
          return;
        }
        const reasonInput = document.querySelector(`[data-cat-reason="${catKey}"]`);
        const reason = reasonInput.value.trim();
        perCategory[catKey] = { status: statusInput.value, desc: reason || baseDesc };
      }

      addUserFood(name, perCategory);
      doSearch();
      return;
    }
    const deleteBtn = e.target.closest("[data-delete-food]");
    if (deleteBtn) {
      deleteUserFood(deleteBtn.dataset.deleteFood);
      doSearch();
    }
  });

  document.getElementById("stageSelect").addEventListener("change", (e) => {
    state.stageIndex = Number(e.target.value);
    state.variantIndex = 0;
    document.getElementById("planResult").classList.add("hidden");
  });

  document.getElementById("generateBtn").addEventListener("click", () => {
    const cat = CATEGORIES[state.category];
    const stage = cat.stages[state.stageIndex];
    const today = todayKey();
    if (state.generated && state.lastGeneratedDateKey === today) {
      // Already showing today's plan for this stage — cycle to another variant on demand.
      state.variantIndex = (state.variantIndex + 1) % stage.meals.length;
    } else {
      // First generate of the day (or a new day since the last one) — start from
      // the date-based pick so the default plan changes automatically day to day.
      state.variantIndex = dailyVariantIndex(stage.key, stage.meals.length);
    }
    state.lastGeneratedDateKey = today;
    state.generated = true;
    renderPlanResult();
  });

  document.body.addEventListener("click", (e) => {
    const btn = e.target.closest(".food-item");
    if (btn) openRecipeModal(btn.dataset.food);
  });

  document.getElementById("modalClose").addEventListener("click", closeRecipeModal);
  document.getElementById("recipeModal").addEventListener("click", (e) => {
    if (e.target.id === "recipeModal") closeRecipeModal();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeRecipeModal();
  });

  document.getElementById("saveBtn").addEventListener("click", () => {
    if (!currentPlanSnapshot) return;
    const list = loadSavedPlans();
    const now = new Date();
    const savedAtLabel = `${now.getFullYear()}.${String(now.getMonth() + 1).padStart(2, "0")}.${String(
      now.getDate()
    ).padStart(2, "0")} 저장`;
    list.push({
      id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
      categoryLabel: currentPlanSnapshot.categoryLabel,
      title: currentPlanSnapshot.title,
      guidance: currentPlanSnapshot.guidance,
      meals: currentPlanSnapshot.meals,
      savedAtLabel,
    });
    writeSavedPlans(list);
    renderSavedList();

    const btn = document.getElementById("saveBtn");
    btn.classList.add("saved");
    document.getElementById("saveBtnLabel").textContent = "저장됨 ✓";
    setTimeout(resetSaveButton, 1500);
  });

  document.getElementById("savedList").addEventListener("click", (e) => {
    const viewBtn = e.target.closest("[data-view]");
    if (viewBtn) {
      const item = loadSavedPlans().find((p) => p.id === viewBtn.dataset.view);
      if (item) {
        showPlanResult({
          categoryLabel: item.categoryLabel,
          title: item.title,
          guidance: item.guidance,
          meals: item.meals,
        });
        document.getElementById("planResult").scrollIntoView({ behavior: "smooth", block: "start" });
      }
      return;
    }
    const delBtn = e.target.closest("[data-delete]");
    if (delBtn) {
      writeSavedPlans(loadSavedPlans().filter((p) => p.id !== delBtn.dataset.delete));
      renderSavedList();
    }
  });

  renderSavedList();
}

init();
