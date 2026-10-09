import 'package:flutter_test/flutter_test.dart';
import 'package:mck_church_app/core/models/role_model.dart';

void main() {
  test('RoleModel parses permissions and checks them', () {
    final role = RoleModel.fromJson({
      'id': '1',
      'name': 'Secretary',
      'is_admin': true,
      'can_act_as_superintendent': false,
      'is_clergy': false,
      'permissions': ['members.view_all'],
    });
    expect(role.hasPermission('members.view_all'), isTrue);
    expect(role.hasPermission('finance.view'), isFalse);
  });
}
