const fs = require('fs');
const path = require('path');

try {
  const content = fs.readFileSync(path.join(__dirname, 'components', 'OddsAnalysisModal.tsx'), 'utf8');
  
  // Count braces
  let openCount = 0;
  let closeCount = 0;
  let stack = [];
  
  for(let i = 0; i < content.length; i++) {
    if(content[i] === '{') {
      openCount++;
      stack.push({char: '{', line: content.substring(0, i).split('\n').length});
    }
    if(content[i] === '}') {
      closeCount++;
      if(stack.length > 0) {
        stack.pop();
      }
    }
  }
  
  console.log('Open braces: ' + openCount);
  console.log('Close braces: ' + closeCount);
  console.log('Difference: ' + (openCount - closeCount));
  
  if(stack.length > 0) {
    console.log('\nUnclosed braces at lines:');
    stack.forEach(item => {
      console.log('Line ' + item.line);
    });
  }
  
} catch(e) {
  console.error('Error:', e.message);
}
