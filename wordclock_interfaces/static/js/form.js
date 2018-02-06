$(document).ready(function() {
    $.ajax({
            url: '/list',
			type : 'POST'
            })
            .done(function(data) {
                $("#pluginDropdown option").remove();
                $.each(data.PLUGINS, function(index, item) {
                    $("#pluginDropdown").append(
                        $("<option></option>")
                            .text(item.PRETTY_NAME)
                            .val(item.NAME)
                    );
                });
            });
    $.ajax({
            url: '/active',
			type : 'POST'
            })
            .done(function(data) {
				$('#pluginList').text(data.PRETTY_NAME + ': ' + data.DESCRIPTION).show();
            });

	$('form').on('submit', function(event) {

		$.ajax({
			data : {
				name : $('#nameInput').val(),
				email : $('#emailInput').val()
			},
			type : 'POST',
			url : '/api'
		})
		.done(function(data) {

			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
				$('#pluginList').text("affe").show();
			}
			else {
				$('#successAlert').text(data.name).show();
				$('#errorAlert').hide();
				$('#pluginList').text("ooo").show();
			}

		});

		event.preventDefault();

	});

});
