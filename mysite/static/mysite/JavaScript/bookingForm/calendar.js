document.addEventListener("DOMContentLoaded", function () {
  const calendar = {
    date: new Date(),
    daySelected: null,
    daysArea: document.querySelector(".calendar__days"),
    displayMonth: document.querySelector("#displayMonth"),
    nextMonthButton: document.querySelector("#nextMonth"),
    previousMonthButton: document.querySelector("#previousMonth"),
    displayYear: document.querySelector("#displayYear"),

    get currentMonth() {
      return this.date.getMonth() + 1;
    },

    get nextMonth() {
      return this.date.getMonth() + 2;
    },

    main() {
      this.nextMonthButton.onclick = (event) => this.handleGoToNextMonth(event);
      this.previousMonthButton.onclick = (event) =>
        this.handleGoToCurrentMonth(event);
      this.handleGoToCurrentMonth();
    },

    handleGoToNextMonth(event) {
      if (event) {
        event.preventDefault();
        event.target.disabled = true;
      }

      const dateNextMonth = new Date(
        this.date.getFullYear(),
        this.nextMonth - 1
      );
      this.displayMonth.innerHTML = dateNextMonth.toLocaleString("default", {
        month: "long",
      });

      const daysInThisMonth = new Date(
        this.date.getFullYear(),
        this.nextMonth,
        0
      ).getDate();
      this.generateDays(daysInThisMonth);

      this.animateFadeOut(this.nextMonthButton);
      this.animateFadeIn(this.previousMonthButton);
      this.previousMonthButton.disabled = false;
    },

    handleGoToCurrentMonth(event) {
      if (event) {
        event.preventDefault();
        event.target.disabled = true;
      }

      this.displayMonth.innerHTML = this.date.toLocaleString("default", {
        month: "long",
      });
      this.displayYear.innerHTML = this.date.getFullYear();

      const daysInThisMonth = new Date(
        this.date.getFullYear(),
        this.currentMonth,
        0
      ).getDate();
      this.generateDays(daysInThisMonth);

      this.animateFadeOut(this.previousMonthButton);
      this.animateFadeIn(this.nextMonthButton);
      this.nextMonthButton.disabled = false;
    },

    async generateDays(daysInThisMonth) {
      this.daysArea.innerHTML = "";
      for (let i = 1; i <= daysInThisMonth; i++) {
        const newButton = document.createElement("button");
        newButton.classList.add("inputInf");
        newButton.innerHTML = i;
        newButton.addEventListener("click", (event) =>
          this.handleSelectDay(event)
        );

        if (i == this.date.getDate()) {
          newButton.classList.add("active");
        }

        this.daysArea.append(newButton);
        await this.sleep(15);
      }
    },

    handleSelectDay(event) {
      event.preventDefault();
      this.removeLastSelected();

      event.target.classList.add("active");
      this.daySelected = Number.parseInt(event.target.innerHTML);
    },

    removeLastSelected() {
      const lastSelected = this.daysArea.querySelector(".active");
      if (lastSelected) lastSelected.classList.remove("active");
    },

    animateFadeIn(element) {
      element.style.display = "block";
      element.classList.add("fadeIn");
      element.onanimationend = () => {
        element.classList.remove("fadeIn");
      };
    },

    animateFadeOut(element) {
      element.classList.add("fadeOut");
      element.onanimationend = () => {
        element.classList.remove("fadeOut");
        element.style.display = "none";
      };
    },

    sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },
  };

  calendar.main();
});
