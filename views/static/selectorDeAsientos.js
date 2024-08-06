document.querySelector('.seat-container').addEventListener('click', function(event) {
    if (event.target.classList.contains('seat') || event.target.tagName === 'I' || event.target.tagName === 'SPAN') {
        const seat = event.target.closest('.seat');
        seat.classList.toggle('selected');
        const selectedSeats = Array.from(document.querySelectorAll('.selected')).map(seat => seat.dataset.seat);
        document.getElementById('selected-seats').value = selectedSeats.join('-');
    }
});