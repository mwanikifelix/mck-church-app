/// Single source of truth for the Django DRF base URL and endpoints.
/// Every path here is confirmed against the actual backend urls.py —
/// not guessed. Add new blocks as each app is wired into the app.
class ApiConfig {
  ApiConfig._();

  // Android emulator -> http://10.0.2.2:8000/api
  // Physical device on same LAN -> http://192.168.x.x:8000/api
  static const String baseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://10.0.2.2:8000/api',
  );

  // --- accounts ---
  static const String login = '$baseUrl/accounts/login/';
  static const String loginRefresh = '$baseUrl/accounts/login/refresh/';
  static const String signup = '$baseUrl/accounts/signup/';
  static const String googleLogin = '$baseUrl/accounts/google/';
  static const String me = '$baseUrl/accounts/me/';
  static const String meQr = '$baseUrl/accounts/me/qr/';
  static const String members = '$baseUrl/accounts/members/';
  static const String roles = '$baseUrl/accounts/roles/';
  static const String permissions = '$baseUrl/accounts/permissions/';
  static const String branches = '$baseUrl/accounts/branches/';

  // --- events ---
  static const String events = '$baseUrl/events/';

  // --- content ---
  static const String livestreams = '$baseUrl/content/livestreams/';
  static const String announcements = '$baseUrl/content/announcements/';

  // --- pastoral ---
  static const String clergy = '$baseUrl/pastoral/clergy/';

  // --- membership ---
  static const String membershipCard = '$baseUrl/membership/card/';

  // --- scripture ---
  static const String bibleVersions = '$baseUrl/scripture/bible/versions/';
  static const String bibleBooks = '$baseUrl/scripture/bible/books/';
  static const String bibleVerseReference = '$baseUrl/scripture/bible/verses/reference/';
  static const String hymns = '$baseUrl/scripture/hymns/';

  // --- giving ---
  static const String donations = '$baseUrl/giving/donations/';
  static const String myDonations = '$baseUrl/giving/donations/mine/';
  static const String paybill = '$baseUrl/giving/paybill/';

  // --- groups (growth-track: JCTM/Youth/Main Church) ---
  static const String growthGroups = '$baseUrl/groups/groups/';
  static const String growthGraduations = '$baseUrl/groups/graduations/';

  // --- church (departments) ---
  static const String departments = '$baseUrl/church/departments/';
  static const String departmentPosts = '$baseUrl/church/department-posts/';

  // --- hbc ---
  static const String hbcGroups = '$baseUrl/hbc/';
  static const String myHbc = '$baseUrl/hbc/mine/';

  // --- prayer ---
  static const String prayerRequests = '$baseUrl/prayer/';

  // --- pastoral (counselling) ---
  static const String counsellingRequests = '$baseUrl/pastoral/counselling/';

  // --- registration (catechism) ---
  static const String registrationWindows = '$baseUrl/registration/windows/';
  static const String catechismRegistrations = '$baseUrl/registration/catechism/';

  // --- attendance ---
  static const String attendanceCheckIn = '$baseUrl/attendance/check-in/';
  static const String attendanceMine = '$baseUrl/attendance/mine/';
}
