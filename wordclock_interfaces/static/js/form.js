$(document).ready(function() {
    $.ajax({
            url: '/pluginlist',
			type : 'POST'
            })
            .done(function(data) {
				$('#pluginList').text(data.PLUGINS[0].DESCRIPTION).show();
                $("#pluginDropdown option").remove();
                $.each(data.PLUGINS, function(index, item) {
                    $("#pluginDropdown").append(
                        $("<option></option>")
                            .text(item.PRETTY_NAME)
                            .val(item.NAME)
                    );
                });
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
