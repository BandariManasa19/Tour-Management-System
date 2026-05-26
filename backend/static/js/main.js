document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        if (alert.dataset.autoClose !== 'false') {
            setTimeout(function () {
                alert.classList.add('fade');
                alert.style.opacity = '0';
                setTimeout(function () {
                    alert.remove();
                }, 400);
            }, 4000);
        }
    });

    const forms = document.querySelectorAll('form[data-validate="true"]');
    forms.forEach(function (form) {
        form.addEventListener('submit', function () {
            const button = form.querySelector('button[type="submit"]');
            if (button) {
                button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
                button.disabled = true;
            }
        });
    });

    const bookingPage = document.querySelector('[data-booking-page="true"]');
    if (bookingPage) {
        const travelersInput = document.getElementById('num_people');
        const totalDisplay = document.getElementById('booking-total');
        const pricePerPerson = Number(bookingPage.dataset.pricePerPerson || 0);
        const deadline = bookingPage.dataset.paymentDeadline;
        const timerBadge = document.getElementById('payment-timer');
        const payButton = document.getElementById('pay-now-button');
        const expiredNote = document.getElementById('payment-expired-note');

        function updateTotal() {
            const travelers = Math.max(1, parseInt(travelersInput.value || '1', 10));
            totalDisplay.textContent = '₹' + (travelers * pricePerPerson).toFixed(2);
        }

        if (travelersInput) {
            travelersInput.addEventListener('input', updateTotal);
            updateTotal();
        }

        if (deadline && timerBadge) {
            const endTime = new Date(deadline).getTime();

            const tick = function () {
                const remaining = endTime - Date.now();

                if (remaining <= 0) {
                    timerBadge.textContent = 'Payment window closed';
                    timerBadge.className = 'badge bg-danger text-white';
                    if (payButton) {
                        payButton.disabled = true;
                        payButton.textContent = 'Payment window closed';
                    }
                    if (expiredNote) {
                        expiredNote.classList.remove('d-none');
                    }
                    return;
                }

                const minutes = Math.floor(remaining / 60000);
                const seconds = Math.floor((remaining % 60000) / 1000);
                timerBadge.textContent = String(minutes).padStart(2, '0') + ':' + String(seconds).padStart(2, '0');
                timerBadge.className = 'badge bg-warning text-dark';
            };

            tick();
            setInterval(tick, 1000);
        }
    }

    const cancelButtons = document.querySelectorAll('[data-cancel-booking]');
    const cancelModal = document.getElementById('cancelBookingModal');
    const cancelForm = document.getElementById('cancelBookingForm');
    const bookingTitle = document.getElementById('cancel-booking-title');

    if (cancelButtons.length && cancelModal && cancelForm) {
        const modal = new bootstrap.Modal(cancelModal);

        cancelButtons.forEach(function (button) {
            button.addEventListener('click', function () {
                const bookingId = button.dataset.bookingId;
                bookingTitle.textContent = button.dataset.bookingTitle;
                cancelForm.action = button.dataset.cancelUrl.replace('/0', '/' + bookingId);
                modal.show();
            });
        });
    }
});
