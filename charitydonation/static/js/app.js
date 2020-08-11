document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;

            console.log(page);
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;


            this.$step.parentElement.hidden = this.currentStep >= 6;

            // TODO: get data from inputs and show them in summary

            const formularz = document.querySelector('form')

            if (this.currentStep === 3){
                const categories = formularz.querySelectorAll('input[type="checkbox"]:checked')
                const institutions = formularz.querySelectorAll('.institution')
                console.log(institutions)
                for (let i=0; i < institutions.length; i++){
                    institutions[i].style.display = 'None'
                    for (let j=0; j < categories.length; j++){
                        if (categories[j].value.toLowerCase() in institutions[i].dataset) {
                            institutions[i].style.display = 'block'
                        }
                    }
                }

            }

            if (this.currentStep === 5) {
                const bagsQuantity = formularz.elements.bags.value;
                const institutionName = formularz.elements.organization.value;
                const address = formularz.elements.address.value;
                const city = formularz.elements.city.value;
                const postcode = formularz.elements.postcode.value;
                const phone = formularz.elements.phone.value;
                const data = formularz.elements.data.value;
                const time = formularz.elements.time.value;
                const moreInfo = formularz.elements.more_info.value;

                const categories = formularz.querySelectorAll('input[name=categories]:checked');
                const dataFields = formularz.querySelectorAll('.summary--text');
                const summaryInformations = formularz.querySelectorAll('.summary')

                let categoriesText = ''

                for (let i = 0; i < categories.length; i++) {
                    categoriesText = categoriesText + categories[i].value
                    if (i !== categories.length - 1) {
                        categoriesText = categoriesText + ', '
                    }
                }

                const quantityText = 'Oddajesz ' + bagsQuantity + ' worki ' + categoriesText

                dataFields[0].innerHTML = quantityText
                dataFields[1].innerHTML = 'Dla ' + institutionName
                console.log(summaryInformations[0])
                const listElements = summaryInformations[0].getElementsByTagName('li')
                listElements[2].innerHTML = address
                listElements[3].innerHTML = city
                listElements[4].innerHTML = postcode
                listElements[5].innerHTML = phone
                listElements[6].innerHTML = data
                listElements[7].innerHTML = time
                listElements[8].innerHTML = moreInfo
            }
        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        submit(e) {
            // e.preventDefault();
            // this.currentStep++;
            // this.updateForm();
        }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }

    const buttons = document.querySelectorAll('.donation-button')
    for (let i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener('click', function (event) {
            $.ajax({
                url: '/take',
                data: {'organization': this.parentElement.parentElement.children[0].innerText},
                type: 'GET',
                dataType: 'json'
            }).done(function (data) {
                $(document).on('click', '.donation-button', function (){
                    this.parentElement.parentElement.style.color='green'
                    this.style.display='none'
                })
            })

        })
    }

    // password validation
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');
    const passwordToEdit = document.querySelector('.edit-password')
    console.log(passwordToEdit)
    passwordToEdit.addEventListener('keyup', function (event){
        $.ajax({
            url: '/password-confirmation',
            data: {'password': this.children[0].value, 'csrfmiddlewaretoken': csrftoken},
            type: 'POST',
            dataType: 'json'
        }).done(function (data){
            if (data === 'correct-password') {
                const editButton = document.querySelector('.edit-button')
                editButton.disabled = false
            }
        })
    })
});