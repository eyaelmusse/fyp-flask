/*
 * This file was automatically generated by EvoSuite
 * Mon Aug 28 01:53:15 GMT 2023
 */

package net.kencochrane.a4j.beans;

import org.junit.Test;
import static org.junit.Assert.*;
import net.kencochrane.a4j.beans.CustomerReview;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.junit.runner.RunWith;

@RunWith(EvoRunner.class) @EvoRunnerParameters(mockJVMNonDeterminism = true, useVFS = true, useVNET = true, resetStaticState = true, separateClassLoader = true, useJEE = true) 
public class CustomerReview_ESTest extends CustomerReview_ESTest_scaffolding {

  @Test(timeout = 4000)
  public void test0()  throws Throwable  {
      CustomerReview customerReview0 = new CustomerReview();
      customerReview0.setComment("[tk`@9.8Rc");
      assertEquals("[tk`@9.8Rc", customerReview0.getComment());
  }

  @Test(timeout = 4000)
  public void test1()  throws Throwable  {
      CustomerReview customerReview0 = new CustomerReview();
      customerReview0.setComment((String) null);
      assertNull(customerReview0.getRating());
  }

  @Test(timeout = 4000)
  public void test2()  throws Throwable  {
      CustomerReview customerReview0 = new CustomerReview();
      customerReview0.setRating("net.kencochrane.a4j.beans.CustomerReview");
      assertNull(customerReview0.getComment());
  }

  @Test(timeout = 4000)
  public void test3()  throws Throwable  {
      CustomerReview customerReview0 = new CustomerReview();
      customerReview0.setSummary("[tk`@9.8Rc");
      assertEquals("[tk`@9.8Rc", customerReview0.getSummary());
  }

  @Test(timeout = 4000)
  public void test4()  throws Throwable  {
      CustomerReview customerReview0 = new CustomerReview();
      String string0 = customerReview0.toString();
      assertEquals("null\nnull\nnull\n", string0);
  }
}
