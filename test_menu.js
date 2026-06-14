const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: "new", args: ['--no-sandbox'] });
  const page = await browser.newPage();
  
  // Set viewport to mobile size
  await page.setViewport({ width: 375, height: 667 });
  
  await page.goto('http://localhost:8080/index.html');
  
  // Wait for the button
  await page.waitForSelector('#mobile-menu-toggle');
  
  console.log("Before click:");
  let menuClass = await page.$eval('#mobile-menu', el => el.className);
  let bodyClass = await page.$eval('body', el => el.className);
  console.log("Menu classes:", menuClass);
  console.log("Body classes:", bodyClass);
  
  console.log("\nClicking toggle button...");
  await page.click('#mobile-menu-toggle');
  
  // Wait a little for any transitions
  await new Promise(r => setTimeout(r, 500));
  
  console.log("\nAfter click:");
  menuClass = await page.$eval('#mobile-menu', el => el.className);
  bodyClass = await page.$eval('body', el => el.className);
  console.log("Menu classes:", menuClass);
  console.log("Body classes:", bodyClass);
  
  await browser.close();
})();
