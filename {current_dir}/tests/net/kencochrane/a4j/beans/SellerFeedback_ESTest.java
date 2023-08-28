/*
 * This file was automatically generated by EvoSuite
 * Mon Aug 28 02:02:50 GMT 2023
 */

package net.kencochrane.a4j.beans;

import org.junit.Test;
import static org.junit.Assert.*;
import static org.evosuite.runtime.EvoAssertions.*;
import net.kencochrane.a4j.beans.FeedBack;
import net.kencochrane.a4j.beans.SellerFeedback;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.junit.runner.RunWith;

@RunWith(EvoRunner.class) @EvoRunnerParameters(mockJVMNonDeterminism = true, useVFS = true, useVNET = true, resetStaticState = true, separateClassLoader = true, useJEE = true) 
public class SellerFeedback_ESTest extends SellerFeedback_ESTest_scaffolding {

  @Test(timeout = 4000)
  public void test0()  throws Throwable  {
      SellerFeedback sellerFeedback0 = new SellerFeedback();
      FeedBack[] feedBackArray0 = new FeedBack[1];
      sellerFeedback0.setFeedback(feedBackArray0);
      String string0 = sellerFeedback0.toString();
      assertEquals("null\n# of feedbacks = 1", string0);
  }

  @Test(timeout = 4000)
  public void test1()  throws Throwable  {
      SellerFeedback sellerFeedback0 = new SellerFeedback();
      // Undeclared exception!
      try { 
        sellerFeedback0.getFeedback();
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("net.kencochrane.a4j.beans.SellerFeedback", e);
      }
  }

  @Test(timeout = 4000)
  public void test2()  throws Throwable  {
      SellerFeedback sellerFeedback0 = new SellerFeedback();
      String string0 = sellerFeedback0.toString();
      assertEquals("feedbacks is null ", string0);
  }
}
