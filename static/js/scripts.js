function showToast(message, type = 'success') {
	const background = type === 'success' ? '#4CAF50' : '#F44336';

	Toastify({
		text: message,
		duration: 3000,
		close: true,
		gravity: "top",
		position: "right",
		backgroundColor: background,
		stopOnFocus: true
	}).showToast();
}