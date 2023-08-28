/*
 * This file was automatically generated by EvoSuite
 * Mon Aug 28 02:07:12 GMT 2023
 */

package net.kencochrane.a4j.beans;

import org.junit.Test;
import static org.junit.Assert.*;
import static org.evosuite.runtime.EvoAssertions.*;
import net.kencochrane.a4j.beans.ThirdPartyProductDetails;
import net.kencochrane.a4j.beans.ThirdPartyProductInfo;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.junit.runner.RunWith;

@RunWith(EvoRunner.class) @EvoRunnerParameters(mockJVMNonDeterminism = true, useVFS = true, useVNET = true, resetStaticState = true, separateClassLoader = true, useJEE = true) 
public class ThirdPartyProductInfo_ESTest extends ThirdPartyProductInfo_ESTest_scaffolding {

  @Test(timeout = 4000)
  public void test0()  throws Throwable  {
      ThirdPartyProductInfo thirdPartyProductInfo0 = new ThirdPartyProductInfo();
      ThirdPartyProductDetails[] thirdPartyProductDetailsArray0 = new ThirdPartyProductDetails[2];
      thirdPartyProductInfo0.setThirdPartyProductDetails(thirdPartyProductDetailsArray0);
      String string0 = thirdPartyProductInfo0.toString();
      assertEquals("null\nnull\n# of productOffers = 2", string0);
  }

  @Test(timeout = 4000)
  public void test1()  throws Throwable  {
      ThirdPartyProductInfo thirdPartyProductInfo0 = new ThirdPartyProductInfo();
      // Undeclared exception!
      try { 
        thirdPartyProductInfo0.getThirdPartyProductDetails();
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("net.kencochrane.a4j.beans.ThirdPartyProductInfo", e);
      }
  }

  @Test(timeout = 4000)
  public void test2()  throws Throwable  {
      ThirdPartyProductInfo thirdPartyProductInfo0 = new ThirdPartyProductInfo();
      String string0 = thirdPartyProductInfo0.toString();
      assertEquals("productOffers is null ", string0);
  }
}
