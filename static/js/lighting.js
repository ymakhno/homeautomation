window.Lighters = function() {
    var lighters = [];
    var self = this;

    var initialize = function() {
        $("#lights_table tbody > tr").each(function(i, obj) {
            lighters.push(new Lighter(self, obj))
        });
    };

    var do_update = function(res) {
        for (var i = 0; i < lighters.length; i++) {
            lighters[i].apply(res[i][0], res[i][1]);
        }
    };

    this.update_lights = function() {
        $.get("lights", function(res) {
            do_update(res);
        })
    };

    this.on = function(lighter, value) {
        if (value === undefined) {
            value = 255;
        }
        $.post("lights", {"id" : lighter.get_id(), "value" : value}, function(res) {
            do_update(res);
        });
    };

    this.off = function(lighter) {
        $.post("lights", {"id" : lighter.get_id(), "value" : 0}, function(res) {
            do_update(res);
        });
    };

    initialize();
};

window.Lighter = function(lighters, table_row) {
    var self = this;
    var $row = $(table_row);
    var _id = $(".lighter_id", table_row).val();
    var _state = 0;
    var _dimmer = 0;
    var _lighters = lighters;
    var $state_buttons;
    var $slider;

    var initialize = function() {
        $row.removeClass('warning');
        $state_buttons = $row.find("td > div.btn-group");
        $slider = $row.find("td > input.slider");
        if ($slider.length !== 0) {
            $slider.slider();
        }
    };

    var clear_state = function() {
        $row.removeClass("warning");
        $state_buttons.children().addClass('btn-primary').off('click');
        if ($slider.length !== 0) {
            $slider.slider('setValue', 0).off('slideStop');
        }
    };

    this.get_id = function() {
        return _id;
    };

    this.apply = function(state, dimmer) {
        clear_state();
        _state = state;
        _dimmer = dimmer;
        if (state == 1) {
            $row.addClass('warning');
            $("button:nth-child(2)", $state_buttons).removeClass("btn-primary")
                .click(function() { _lighters.off(self); return false; });
        } else {
            $("button:nth-child(1)", $state_buttons).removeClass("btn-primary")
                .click(function() { _lighters.on(self); return false; });
        }
        if ($slider.length !== 0) {
            $slider.slider('setValue', dimmer);
            var handle = true;
            $slider.on('slideStop', function(e) {
                if (handle) {
                    _lighters.on(self, e.value);
                }
                handle = !handle;
            });
        }
    };

    initialize();
};

$(document).ready(function() {
    var lighters = new Lighters();
    lighters.update_lights();
    setInterval(function() {
        lighters.update_lights();
    }, 20000);

    $("#rule_form").submit(function() {
        var ruleForm = $("#rule_form");
        $("#new_rule input").each(function(i, obj) {
            var $obj = $(obj);
            var id = $obj.attr("id");
            if (id !== undefined) {
                if ($obj.attr("type") == "checkbox") {
                    $("input[name='" + id + "']", ruleForm).val($obj.parent().hasClass("active"))
                } else {
                    $("input[name='" + id + "']", ruleForm).val($(obj).val());
                }
            }
        });
        $("input[name='rule_lighter']", ruleForm).val($("#rule_lighter").val());
    })
});