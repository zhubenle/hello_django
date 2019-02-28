let users_obj = {
    csrfToken: $("[name=csrfmiddlewaretoken]").val(),
    url_page_users: $('#url_page_users').val(),
    url_page_roles: $('#url_page_roles').val(),
    url_add_user: $('#url_add_user').val(),
    url_update_user: $('#url_update_user').val(),
    tableUsers: null,
    init: function (_opt) {
        users_obj.tableUsers = $('#table_users').DataTable({
            serverSide: true,
            processing: true,
            searching: true,
            autoWidth: false,
            language: {
                lengthMenu: 'Show _MENU_'
            },
            searchDelay: 2000,
            ajax: {
                url: users_obj.url_page_users,
                type: 'POST',
                data: {csrfmiddlewaretoken: users_obj.csrfToken},
                dataFilter: function (resp) {
                    resp = $.parseJSON(resp);
                    if (resp.code === 10000) {
                        return JSON.stringify(resp.data);
                    }
                    return JSON.stringify({'error': resp.msg});
                }
            },
            createdRow: function (tr, data, dataIndex, tds) {
                let append_html = '<td><button class="btn btn-primary btn-sm" onclick="users_obj.edit_user(' + data.id + ')">Edit</button> ';
                if (data.del_status) {
                    append_html += '<button class="btn btn-warning btn-sm" onclick="users_obj.enable_user(' + data.id + ')">Enable</button>';
                } else {
                    append_html += '<button class="btn btn-danger btn-sm" onclick="users_obj.disable_user(' + data.id + ')">Disable</button>';
                }
                append_html += '</td>';
                $(tr).append(append_html);
            },
            columns: [
                {data: 'id'},
                {data: 'username'},
                {data: 'real_name'},
                {data: 'phone'},
                {data: 'email'},
                {data: 'last_login_ip', searchable: false},
                {data: 'last_login_time', searchable: false},
                {data: 'update_time', searchable: false},
                {data: 'create_time', searchable: false},
                {
                    data: 'del_status',
                    searchable: false,
                    createdCell: function (td, cellData, rowData, row, col) {
                        let style = cellData ? 'label-danger' : 'label-info';
                        $(td).html('<lable class="label ' + style + '">' + cellData + '</lable>');
                    }
                }
            ],
        });
        //------------add user start------------
        let add_input_username = $('#add_input_username');
        let add_input_password = $('#add_input_password');
        let add_input_cfm_password = $('#add_input_cfm_password');
        let add_input_real_name = $('#add_input_real_name');
        let add_input_email = $('#add_input_email');
        let add_input_phone = $('#add_input_phone');
        let add_select_roles = $('#add_select_roles');
        let btn_model_add_user = $('#btn_model_add_user');
        let modal_add = $('#modal_add');
        let btn_modal_add_submit = $('#btn_modal_add_submit');

        let add_select_roles_select2 = add_select_roles.select2({
            placeholder: 'Select roles',
            maximumSelectionLength: 3,
            delay: 300,
            allowClear: true,
            ajax: {
                url: users_obj.url_page_roles,
                method: 'POST',
                dataType: 'JSON',
                data: function (params) {
                    return {
                        csrfmiddlewaretoken: users_obj.csrfToken,
                        page_no: params.page || 1
                    }
                },
                processResults: function (resp, params) {
                    if (resp.code === 10000) {
                        params.page = params.page || 1;
                        return {
                            "results": $.map(resp.data.data, function (role) {
                                return {
                                    "id": role.id,
                                    "text": role.name
                                }
                            }),
                            "pagination": {
                                "more": 10 * params.page < resp.data.recordsTotal
                            }
                        }
                    } else {
                        return null;
                    }
                }
            }
        });

        function add_clear() {
            //清空添加模态框中的数据
            add_input_username.val('');
            add_input_password.val('');
            add_input_cfm_password.val('');
            add_input_real_name.val('');
            add_input_email.val('');
            add_input_phone.val('');
            add_select_roles_select2.val(null).trigger('change');
            modal_add.find('.form-group').removeClass('has-error').removeClass('has-success')
                .find('span > i').removeClass('fa-times').removeClass('fa-check')
        }

        modal_add.on('hidden.bs.modal', function (e) {
            add_clear();
        });

        btn_modal_add_submit.on('click', function () {
            let is_submit = true;
            let username = $.trim(add_input_username.val());
            if (!username || username.length < 8 || username.length > 20) {
                add_input_username.parents('.form-group').addClass('has-error')
                    .find('span > i').addClass('fa-times');
                is_submit = false;
            }
            let password = $.trim(add_input_password.val());
            if (!password || password.length < 8 || password.length > 32) {
                add_input_password.parents('.form-group').addClass('has-error')
                    .find('span > i').addClass('fa-times');
                is_submit = false;
            }
            let cfm_password = $.trim(add_input_cfm_password.val());
            if (cfm_password !== password) {
                add_input_cfm_password.parents('.form-group').addClass('has-error')
                    .find('span > i').addClass('fa-times');
                is_submit = false;
            }
            let real_name = $.trim(add_input_real_name.val());
            if (!real_name || real_name.length > 20) {
                add_input_real_name.parents('.form-group').addClass('has-error')
                    .find('span > i').addClass('fa-times');
                is_submit = false;
            }
            let email = $.trim(add_input_email.val());
            if (!email || email.length > 32) {
                add_input_email.parents('.form-group').addClass('has-error')
                    .find('span > i').addClass('fa-times');
                is_submit = false;
            }
            let phone = $.trim(add_input_phone.val());
            if (!phone || phone.length > 32) {
                add_input_phone.parents('.form-group').addClass('has-error')
                    .find('span > i').addClass('fa-times');
                is_submit = false;
            }
            let roles = add_select_roles_select2.val();
            if (!roles || roles.length < 1) {
                add_select_roles.parents('.form-group').addClass('has-error')
                    .find('span > i').addClass('fa-times');
                is_submit = false;
            }
            if (is_submit) {
                $.ajax(users_obj.url_add_user, {
                    method: 'POST',
                    dataType: 'JSON',
                    data: {
                        csrfmiddlewaretoken: users_obj.csrfToken,
                        username: username,
                        password: password,
                        real_name: real_name,
                        email: email,
                        phone: phone,
                        roles: roles.join(',')
                    },
                    success: function (resp) {
                        if (resp.code === 10000) {
                            modal_add.modal('hide');
                            swal('Success', 'User add success', 'success').then(function () {
                                users_obj.tableUsers.draw();
                            });
                        } else {
                            swal('Fail', 'User add fail: ' + resp.msg, 'error')
                        }
                    },
                    error: function (xhr, ts, et) {
                        swal('Fail', 'User add error: ' + et, 'error');
                    }
                });
            }
        });
        //------------add user end------------
    },
    disable_user: function (id) {
        swal({
            title: 'Are you sure?',
            text: 'You are disabling user! the id is ' + id,
            icon: 'warning',
            buttons: true,
            dangerMode: true,
        }).then(function (will_disable) {
            if (will_disable) {
                $.ajax(users_obj.url_update_user, {
                    method: 'POST',
                    dataType: 'JSON',
                    data: {
                        csrfmiddlewaretoken: users_obj.csrfToken,
                        id: id,
                        del_status: true
                    },
                    success: function (resp) {
                        if (resp.code === 10000) {
                            swal('Success', 'User disable success', 'success').then(function () {
                                users_obj.tableUsers.draw();
                            });
                        } else {
                            swal('Fail', 'User disable fail: ' + resp.msg, 'error')
                        }
                    },
                    error: function (xhr, ts, et) {
                        swal('Fail', 'User disable error: ' + et, 'error');
                    }
                })
            }
        });
    },
    enable_user: function (id) {
        swal({
            title: 'Are you sure?',
            text: 'You are enabling user! the id is ' + id,
            icon: 'warning',
            buttons: true,
            dangerMode: true,
        }).then(function (will_enable) {
            if (will_enable) {
                $.ajax(users_obj.url_update_user, {
                    method: 'POST',
                    dataType: 'JSON',
                    data: {
                        csrfmiddlewaretoken: users_obj.csrfToken,
                        id: id,
                        del_status: false
                    },
                    success: function (resp) {
                        if (resp.code === 10000) {
                            swal('Success', 'User enable success', 'success').then(function () {
                                users_obj.tableUsers.draw();
                            });
                        } else {
                            swal('Fail', 'User enable fail: ' + resp.msg, 'error')
                        }
                    },
                    error: function (xhr, ts, et) {
                        swal('Fail', 'User enable error: ' + et, 'error');
                    }
                })
            }
        });
    },
    edit_user: function (id) {

    }
};