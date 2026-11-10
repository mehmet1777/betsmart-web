// Test API response
const response = await fetch('http://localhost:3000/api/matches');
const data = await response.json();

console.log('API Response:');
console.log('Success:', data.success);
console.log('Count:', data.count);
console.log('Matches:', JSON.stringify(data.matches, null, 2));

if (data.error) {
  console.error('Error:', data.error);
}
