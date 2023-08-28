/*
 * This file was automatically generated by EvoSuite
 * Mon Aug 28 01:52:40 GMT 2023
 */

package net.kencochrane.a4j.beans;

import org.junit.Test;
import static org.junit.Assert.*;
import static org.evosuite.runtime.EvoAssertions.*;
import java.util.ArrayList;
import net.kencochrane.a4j.beans.BlendedSearch;
import net.kencochrane.a4j.beans.ProductLine;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.junit.runner.RunWith;

@RunWith(EvoRunner.class) @EvoRunnerParameters(mockJVMNonDeterminism = true, useVFS = true, useVNET = true, resetStaticState = true, separateClassLoader = true, useJEE = true) 
public class BlendedSearch_ESTest extends BlendedSearch_ESTest_scaffolding {

  @Test(timeout = 4000)
  public void test0()  throws Throwable  {
      BlendedSearch blendedSearch0 = new BlendedSearch();
      ArrayList<ProductLine> arrayList0 = new ArrayList<ProductLine>();
      ProductLine productLine0 = new ProductLine();
      arrayList0.add(productLine0);
      blendedSearch0.productLines = arrayList0;
      // Undeclared exception!
      try { 
        blendedSearch0.printProductList();
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("net.kencochrane.a4j.beans.ProductLine", e);
      }
  }

  @Test(timeout = 4000)
  public void test1()  throws Throwable  {
      BlendedSearch blendedSearch0 = new BlendedSearch();
      ArrayList<ProductLine> arrayList0 = new ArrayList<ProductLine>();
      blendedSearch0.productLines = arrayList0;
      String string0 = blendedSearch0.printProductList();
      assertEquals("# of productLines = 0\n", string0);
  }

  @Test(timeout = 4000)
  public void test2()  throws Throwable  {
      BlendedSearch blendedSearch0 = new BlendedSearch();
      ArrayList<ProductLine> arrayList0 = new ArrayList<ProductLine>();
      ProductLine productLine0 = new ProductLine();
      arrayList0.add(productLine0);
      blendedSearch0.productLines = arrayList0;
      String string0 = blendedSearch0.toString();
      assertEquals("Mode = null\nnull\n\n# of productLines = 1\n", string0);
  }

  @Test(timeout = 4000)
  public void test3()  throws Throwable  {
      BlendedSearch blendedSearch0 = new BlendedSearch();
      String string0 = blendedSearch0.toString();
      assertEquals("productLines is null \n", string0);
  }

  @Test(timeout = 4000)
  public void test4()  throws Throwable  {
      BlendedSearch blendedSearch0 = new BlendedSearch();
      ProductLine[] productLineArray0 = new ProductLine[4];
      blendedSearch0.setProductLine(productLineArray0);
      assertEquals(4, productLineArray0.length);
  }

  @Test(timeout = 4000)
  public void test5()  throws Throwable  {
      BlendedSearch blendedSearch0 = new BlendedSearch();
      String string0 = blendedSearch0.printProductList();
      assertEquals("productLines is null \n", string0);
  }

  @Test(timeout = 4000)
  public void test6()  throws Throwable  {
      BlendedSearch blendedSearch0 = new BlendedSearch();
      // Undeclared exception!
      try { 
        blendedSearch0.getProductLine();
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("net.kencochrane.a4j.beans.BlendedSearch", e);
      }
  }
}
